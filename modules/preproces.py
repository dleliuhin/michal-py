import cv2
import numpy as np
from config.config import Config
from modules.hough import *
from modules.convex_hull import *
from modules.base import *
from modules.evaluate import *


# =====================================================================================================================
def detect_puncture(src, template, cfg):

    # Preproccessing
    tmp = src.copy()
    denoise(tmp, cv2.MORPH_OPEN, cfg)

    # Detect the puncture center
    center_result = detect_by_template(tmp, template, cfg)

    if cfg.trace:
        print('Template matched')

    center = center_result.center
    result_hough = Result()
    result_convex = Result()

    # Fill the center star
    denoise(tmp, cv2.MORPH_CLOSE, cfg)
    kernel = cv2.getStructuringElement(cfg.kernel_shape, (cfg.center_fill_size, cfg.center_fill_size))
    tmp = cv2.erode(tmp, kernel, 5)

    h, w = tmp.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    cv2.floodFill(tmp, mask, (int(center.x), int(center.y)), 0)

    # Fill small areas (remove possible inner lines)
    denoise(tmp, cv2.MORPH_CLOSE, cfg)

    if cfg.trace:
        print('Denoised')

    if cfg.gui:
        pdenoised = cv2.cvtColor(tmp, cv2.COLOR_GRAY2RGB)
        pdenoised = cv2.resize(pdenoised, (300, 250))
        cv2.imshow('punctured', pdenoised)
        cv2.moveWindow('punctured', 0, 350)

    # Hough + convex hull method
    result_hough = HoughTransf(tmp, center_result.center, cfg)

    if cfg.trace:
        print('Hough Transformed')

    result_convex = ConvexHullMethod(tmp, center, cfg)

    if cfg.trace:
        print('Convex Hulled')

    result = Result()

    if not resultCompare(center, result_hough, result_convex, result, cfg.result_compare_tolerance):
        if result_hough.is_none():
            result = result_convex
        elif result_convex.is_none():
            result = result_hough
        elif result.is_none():
            result = result_convex

    symmetrize(center, result, cfg.symmetrize_tolerance)

    if cfg.trace:
        print('Symmetrized')

    return [result, True]
# =====================================================================================================================


# =====================================================================================================================
def denoise(src, operation, cfg):
    # invert image
    cv2.bitwise_not(src, src)
    kernel = cv2.getStructuringElement(cfg.kernel_shape, (cfg.kernel_size, cfg.kernel_size))
    cv2.morphologyEx(src, operation, kernel, src)
    # return image invertion back to normal
    cv2.bitwise_not(src, src)
# =====================================================================================================================


# =====================================================================================================================
def detect_by_template(src, template, cfg):

    # Detect the template position
    img = template_detect(src, template, cfg.match_method)

    # Localize the best match position
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
    matchLoc = maxLoc

    # For SQDIFF and SQDIFF_NORMED, the best matches are lower values.
    if cfg.match_method == cv2.TM_SQDIFF or cfg.match_method == cv2.TM_SQDIFF_NORMED:
        matchLoc = minLoc

    if cfg.gui:
        pdenoised = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
        cv2.line(pdenoised,
                 (int(matchLoc[0] + template.shape[1] / 2), matchLoc[1]),
                 (int(matchLoc[0] + template.shape[1] / 2), matchLoc[1] + template.shape[0]),
                 (0, 255, 0), 4, 8, 0)
        cv2.line(pdenoised,
                 (matchLoc[0], int(matchLoc[1] + template.shape[0] / 2)),
                 (matchLoc[0] + template.shape[1], int(matchLoc[1] + template.shape[0] / 2)),
                 (0, 255, 0), 4, 8, 0)
        pdenoised = cv2.resize(pdenoised, (300, 250))
        cv2.imshow('centered', pdenoised)
        cv2.moveWindow('centered', 1400, 0)

    return Result(matchLoc[1], matchLoc[1] + template.shape[0], matchLoc[0], matchLoc[0] + template.shape[1])
# =====================================================================================================================


# =====================================================================================================================
def template_detect(src, template, match_method):

    # Do the matching and normalize result
    res = cv2.matchTemplate(cv2.cvtColor(src, cv2.COLOR_GRAY2RGB), template, match_method)
    cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, - 1)

    return res
# =====================================================================================================================
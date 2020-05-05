import cv2
import numpy as np
from config.config import Config
from modules.hough import HoughTransf
from modules.base import Result


def detect_puncture(src: np.ndarray, template: np.ndarray, cfg: Config):
    tmp = src.copy()
    denoise(tmp, cv2.MORPH_OPEN, cfg)
    res = detect_by_template(tmp, template, cfg)

    denoise(tmp, cv2.MORPH_CLOSE, cfg)
    kernel = cv2.getStructuringElement(cfg.kernel_shape, (cfg.center_fill_size, cfg.center_fill_size))
    tmp = cv2.erode(tmp, kernel, 5)

    h, w = tmp.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    cv2.floodFill(tmp, mask, res.center, 0)

    denoise(tmp, cv2.MORPH_CLOSE, cfg)

    if cfg.gui:
        pdenoised = cv2.cvtColor(tmp, cv2.COLOR_GRAY2RGB)
        pdenoised = cv2.resize(pdenoised, (300, 250))
        cv2.imshow('punctured', pdenoised)
        cv2.moveWindow('punctured', 0, 350)

    HoughTransf(tmp, res.center, cfg)

    return res


def denoise(src: np.ndarray, operation: int, cfg: Config):
    cv2.bitwise_not(src, src)
    kernel = cv2.getStructuringElement(cfg.kernel_shape, (cfg.kernel_size, cfg.kernel_size))
    cv2.morphologyEx(src, operation, kernel, src)
    cv2.bitwise_not(src, src)


def detect_by_template(src: np.ndarray, template: np.ndarray, cfg: Config) -> Result:
    img = template_detect(src, template, cfg.match_method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
    matchLoc = maxLoc
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


def template_detect(src: np.ndarray, template: np.ndarray, match_method: int):
    res = cv2.matchTemplate(cv2.cvtColor(src, cv2.COLOR_GRAY2RGB), template, match_method)
    cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, - 1)

    return res

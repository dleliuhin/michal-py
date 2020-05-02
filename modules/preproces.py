import cv2
import numpy as np
from config.config import Config


def detect_puncture(src, template, cfg):
    denoise(src, cv2.MORPH_OPEN, cfg)
    res = detect_by_template(src, template, cfg.match_method)

    pdenoised = cv2.resize(res, (300, 250))
    cv2.imshow('denoised', pdenoised)
    cv2.moveWindow('denoised', 0, 400)

    return res


def denoise(src, operation, cfg):
    cv2.bitwise_not(src, src)
    kernel = cv2.getStructuringElement(cfg.kernel_shape,
                                       (cfg.kernel_size, cfg.kernel_size))
    cv2.morphologyEx(src, operation, kernel)
    cv2.bitwise_not(src, src)


def detect_by_template(src, template, match_method):
    img = template_detect(src, template, match_method)
    # minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
    # matchLoc = maxLoc
    # if match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED:
    #     matchLoc = minLoc

    # return matchLoc[1], matchLoc[1] + template[0], matchLoc[0], matchLoc[0] + template[1]
    return img


def template_detect(src, template, match_method):
    res = cv2.matchTemplate(src, template, match_method)
    cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, - 1)

    return res

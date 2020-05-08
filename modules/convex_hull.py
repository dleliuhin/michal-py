import cv2
import numpy as np
from config.config import Config
from modules.base import *


# =====================================================================================================================
def ConvexHullMethod(src, center, cfg):

    # input image in gray style with applyed threshold
    res = Result()

    # find  contours in binary image
    contours, hierarchy = cv2.findContours(src, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    hull = [None] * len(contours)

    for i in range(len(contours)):
        # filter small areas
        if cv2.contourArea(contours[i]) > 500:

            # Find the convex hull of a point set.
            hull[i] = cv2.convexHull(contours[i])
            hull[i] = cv2.approxPolyDP(hull[i], 0.1 * cv2.arcLength(hull[i], True), True)

            if len(hull[i]) == 4:
                left = 0
                right = 0
                top = 0
                bottom = 0

                for j in range(len(hull[i])):
                    if hull[i][j][0][0] < hull[i][left][0][0]:
                        left = j
                    if hull[i][j][0][0] > hull[i][right][0][0]:
                        right = j
                    if hull[i][j][0][1] < hull[i][top][0][1]:
                        top = j
                    if hull[i][j][0][1] > hull[i][bottom][0][1]:
                        bottom = j

                if (left != right) and (left != top) and (left != bottom) and (right != top) and (right != bottom) \
                        and (top != bottom) and (hull[i][left][0][0] < center.x) and (hull[i][right][0][0] > center.x) \
                        and (hull[i][top][0][1] < center.y) and (hull[i][bottom][0][1] > center.y):
                    res.setPosition(hull[i][top][0][1], hull[i][bottom][0][1], hull[i][left][0][0], hull[i][right][0][0])
                    break

    if cfg.gui:
        convex = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
        cv2.drawContours(convex, contours, -1, (0, 255, 0), 3)
        cv2.rectangle(convex, (int(res.left), int(res.top)), (int(res.right), int(res.bottom)), (0, 255, 0), 1, 8, 0)
        cv2.imshow('convex', cv2.resize(convex, (300, 250)))
        cv2.moveWindow('convex', 0, 700)

    return res
# =====================================================================================================================

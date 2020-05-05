import cv2
import numpy as np
from config.config import Config
from modules.base import *


def HoughTransf(src: np.ndarray, center, cfg: Config):

    blured = src.copy()
    cv2.bitwise_and(src, blured)
    blured = cv2.GaussianBlur(src, (7, 7), 2.0, 2.0)

    if cfg.gui:
        pblured = cv2.cvtColor(blured, cv2.COLOR_GRAY2RGB)
        pblured = cv2.resize(pblured, (300, 250))
        cv2.imshow('blured', pblured)
        cv2.moveWindow('blured', 350, 350)

    edges = cv2.Canny(blured, 66.0, 133.0, 3)

    if cfg.gui:
        pblured = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        pedges = cv2.resize(edges, (300, 250))
        cv2.imshow('edges', pedges)
        cv2.moveWindow('edges', 700, 350)

    intersections = list()

    # if cfg.probabilistic:
    # minLineLength = 50
    # maxLineGap = 10
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, cfg.hough_threshold, minLineLength, maxLineGap)

        # for x in lines:
        #     for y in lines:
        #         intersections.append(computeIntersect(x, y))
    #
    # else:

    lines = cv2.HoughLines(edges, 1, np.pi / 180, cfg.hough_threshold, 0, 0)
    if cfg.gui:
        hough = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                intersections.append((x0, y0))
                cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 4, 8, 0)
        cv2.imshow('hough', cv2.resize(hough, (300, 250)))
        cv2.moveWindow('hough', 1050, 350)

    # if cfg.gui:
    #     hough = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
    #     for x1, y1, x2, y2 in lines[0]:
    #         cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 6)
    #     cv2.imshow('hough', hough)
        # cv2.moveWindow('hough', 1000, 400)

    # for x in lines[0]:
    #     for y in lines[0]:
    #         if acceptLinePair(x, y, np.pi / 32):
    #             intersections.append(computeIntersect(x, y))

    # if cfg.gui:
    #     pedges = src.copy()
    #
    #     for x1, y1, x2, y2 in lines[0]:
    #         cv2.line(pedges, (x1, y1), (x2, y2), (0, 255, 0), 2)

    gab_tolerance = 0


def computeIntersect(line1, line2) -> list:
    p1 = lineToPointPair(line1)
    p2 = lineToPointPair(line2)

    x1 = p1[0].x
    y1 = p1[0].y
    x2 = p1[1].x
    y2 = p1[1].y
    x3 = p2[0].x
    y3 = p2[0].y
    x4 = p2[1].x
    y4 = p2[1].y

    d = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

    pt = list()
    pt[0] = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    pt[1] = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d

    return pt


def lineToPointPair(line) -> list:
    points = list()

    r = line[0]
    t = line[1]
    cos_t = np.cos(t)
    sin_t = np.sin(t)
    x0 = r * cos_t
    y0 = r * sin_t
    alpha = 1000

    points.append((x0 + alpha * (- sin_t), y0 + alpha * cos_t))
    points.append((x0 - alpha * (- sin_t), y0 - alpha * cos_t))

    return points


def acceptLinePair(line1, line2, minTheta) -> bool:
    theta1 = line1[1]
    theta2 = line2[1]

    if theta1 < minTheta:
        theta1 += np.pi

    if theta2 < minTheta:
        theta2 += np.pi

    return abs(theta1 - theta2) > minTheta

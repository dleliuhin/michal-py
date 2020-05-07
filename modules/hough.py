import cv2
import numpy as np
from config.config import Config
from modules.base import *


# =====================================================================================================================
def HoughTransf(src: np.ndarray, center: Point, cfg: Config) -> Result:

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

    intersections = []

    if cfg.probabilistic:
        minLineLength = 50
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, cfg.hough_threshold, minLineLength, maxLineGap)

        # compute the intersections of the detected lines
        for x in lines:
            for y in lines:
                intersections.append(computeIntersect(x, y))

        if cfg.gui:
            hough = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 6)
            cv2.imshow('hough', cv2.resize(hough, (300, 250)))
            cv2.moveWindow('hough', 1050, 350)

    else:

        lines = cv2.HoughLines(edges, 1, np.pi / 180, cfg.hough_threshold, 0, 0)

        # compute the intersections of the detected lines
        for line in lines:
            for nline in lines:
                if acceptLinePair(line, nline, np.pi / 32):
                    intersections.append(computeIntersect(line, nline))

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
                    cv2.line(hough, (x1, y1), (x2, y2), (0, 255, 0), 4, 8, 0)
            cv2.imshow('hough', cv2.resize(hough, (300, 250)))
            cv2.moveWindow('hough', 1050, 350)

    # filter and sort the intersections groups
    group_blocks = sortGroups(intersections.copy(), cfg.groups_min_distance)

    result = Result()

    for i in (0, cfg.max_gab_tolerance, 5):
        if punctureFind(src, group_blocks, center, result, i):
            break

    if cfg.gui:
        inters = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
        for i in intersections:
            cv2.circle(inters, (int(i.x), int(i.y)), 2, (255, 0, 0), 4)
        for g in group_blocks:
            cv2.rectangle(inters,
                          (int(g.position.left), int(g.position.top)),
                          (int(g.position.right), int(g.position.bottom)),
                          (0, 0, 255), 2, 8)
        cv2.line(inters, (int(center.x), int(center.y - 25)), (int(center.x), int(center.y + 25)), (0, 0, 255))
        cv2.line(inters, (int(center.x - 25), int(center.y)), (int(center.x + 25), int(center.y)), (0, 0, 255))
        cv2.rectangle(inters,
                      (int(result.left), int(result.top)),
                      (int(result.right), int(result.bottom)),
                      (0, 255, 0), 1, 8, 0)
        cv2.imshow('inters', cv2.resize(inters, (300, 250)))
        cv2.moveWindow('inters', 1400, 350)

    group_blocks.clear()
    return result
# =====================================================================================================================


# =====================================================================================================================
def computeIntersect(line1, line2) -> Point:
    p1 = lineToPointPair(line1)
    p2 = lineToPointPair(line2)

    x1 = p1[0][0]
    y1 = p1[0][1]
    x2 = p1[1][0]
    y2 = p1[1][1]
    x3 = p2[0][0]
    y3 = p2[0][1]
    x4 = p2[1][0]
    y4 = p2[1][1]

    d = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

    return Point(((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d,
                 ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d)
# =====================================================================================================================


# =====================================================================================================================
def lineToPointPair(line) -> list:
    points = list()

    r = line[0][0]
    t = line[0][1]
    cos_t = np.cos(t)
    sin_t = np.sin(t)
    x0 = r * cos_t
    y0 = r * sin_t
    alpha = 1000

    points.append((x0 + alpha * (- sin_t), y0 + alpha * cos_t))
    points.append((x0 - alpha * (- sin_t), y0 - alpha * cos_t))

    return points
# =====================================================================================================================


# =====================================================================================================================
def acceptLinePair(line1, line2, minTheta) -> bool:
    theta1 = line1[0][1]
    theta2 = line2[0][1]

    if theta1 < minTheta:
        theta1 += np.pi

    if theta2 < minTheta:
        theta2 += np.pi

    return abs(theta1 - theta2) > minTheta
# =====================================================================================================================


# =====================================================================================================================
def sortGroups(points: list, min_distance: float) -> list():

    # sort the lines intersections groups into Groups
    group_blocks = list()
    groups = list()

    points_index = 0
    group_index = 0
    in_group_index = 0

    while len(points) != 0:
        p = points[0]
        g = Group(p.y, p.y, p.x, p.x)
        g.points = 1

        group_i = list()
        groups.append(group_i)
        groups[group_index].append(p)
        points.pop(0)

        in_group_index = 0

        while in_group_index < len(groups[group_index]):
            points_index = 0

            while points_index < len(points):
                p = points[points_index]
                # add points in minimum range distance to current group

                if pointsDistance(groups[group_index][in_group_index], p) <= min_distance:
                    groups[group_index].append(points[points_index])

                    if g.position.top > p.y:
                        g.position.top = p.y
                    if g.position.bottom < p.y:
                        g.position.bottom = p.y
                    if g.position.left > p.x:
                        g.position.left = p.x
                    if g.position.right < p.x:
                        g.position.right = p.x

                    g.points += 1
                    points.pop(points_index)

                else:
                    points_index += 1

            in_group_index += 1

        group_blocks.append(g)
        group_index += 1

    return group_blocks
# =====================================================================================================================


# =====================================================================================================================
def pointsDistance(p1: Point, p2: Point) -> float:
    x = p1.x - p2.x
    y = p1.y - p2.y
    return np.sqrt(x**2 + y**2)
# =====================================================================================================================


# =====================================================================================================================
def punctureFind(img: np.ndarray, group_blocks: list, center: Point, result: Result, gab_tolerance: float) -> bool:

    # Find the puncture position by center and intersections groups
    if len(group_blocks) == 0:
        return False

    top_g = Group()
    bottom_g = Group()
    left_g = Group()
    right_g = Group()

    result.top = 0.0
    result.bottom = 10 * center.y
    result.left = 0.0
    result.right = 10 * center.x
    result.center = Point(0.0, 0.0)

    for g in group_blocks:
        if (g.position.left - gab_tolerance < center.x) and (g.position.right + gab_tolerance > center.x):
            if (g.position.bottom < center.y) and (g.position.bottom > result.top):
                result.top = g.position.bottom
                top_g = g

            if (g.position.top > center.y) and (g.position.top < result.bottom):
                result.bottom = g.position.top
                bottom_g = g

        if (g.position.top - gab_tolerance < center.y) and (g.position.bottom + gab_tolerance > center.y):
            if (g.position.right < center.x) and (g.position.right > result.left):
                result.left = g.position.right
                left_g = g

            if (g.position.left > center.x) and (g.position.left < result.right):
                result.right = g.position.left
                right_g = g

    if top_g.nis_none() and bottom_g.nis_none() and left_g.nis_none() and right_g.nis_none():
        white_extension = 5

        if top_g.position.left is not None and bottom_g.position.right is not None:
            while whiteLineArea(img,
                                Point(top_g.position.left - white_extension, result.top + 1),
                                Point(top_g.position.right + white_extension, result.top + 1)):
                result.top += 1

        if bottom_g.position.left is not None and bottom_g.position.right is not None:
            while whiteLineArea(img,
                                Point(bottom_g.position.left - white_extension, result.bottom - 1),
                                Point(bottom_g.position.right + white_extension, result.bottom - 1)):
                result.bottom -= 1

        if left_g.position.top is not None and left_g.position.bottom is not None:
            while whiteLineArea(img,
                                Point(result.left + 1, left_g.position.top - white_extension),
                                Point(result.left + 1, left_g.position.bottom + white_extension)):
                result.left += 1

        if right_g.position.top is not None and right_g.position.bottom is not None:
            while whiteLineArea(img,
                                Point(result.right - 1, right_g.position.top - white_extension),
                                Point(result.right - 1, right_g.position.bottom + white_extension)):
                result.right -= 1

        return True

    else:
        return False
# =====================================================================================================================


# =====================================================================================================================
def whiteLineArea(img: np.ndarray, fr: Point, to: Point) -> bool:

    # check for white space between two points
    horizontal = int(fr.y) == int(to.y)

    i_start = float
    i_end = float
    if horizontal:
        i_start = 0 if fr.x < 0 else fr.x
        i_end = img.shape[1] - 1 if to.x >= img.shape[1] else to.x

    else:
        i_start = 0 if fr.y < 0 else fr.y
        i_end = img.shape[0] - 1 if to.y >= img.shape[0] else to.y

    j = int(fr.y if horizontal else fr.x)

    if 0 <= j < img.shape[0]:
        for i in range(int(i_start), int(i_end)):
            if horizontal:
                if img.item((j, i)) == 0:
                    el = img.item((j, i))
                    return False

            else:
                if img.item((i, j)) == 0:
                    el = img.item((i, j))
                    return False

    return True
# =====================================================================================================================
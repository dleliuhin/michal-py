import cv2
import numpy as np
from config.config import Config
from modules.base import *


# =====================================================================================================================
def resultCompare(center, result_hough, result_convex, result, tolerance):

    if result_hough.top == 0 and result_hough.bottom == 0 and result_hough.left == 0 and result_hough.right == 0:
        return False

    if result_convex.top == 0 and result_convex.bottom == 0 and result_convex.left == 0 and result_convex.right == 0:
        return False

    dist = result_hough.top - result_convex.top

    if abs(dist) > tolerance:

        # top doesn't match
        dist = result_hough.bottom - result_convex.bottom

        if abs(dist) > tolerance:
            # bottom also doesn't mach - detection unsuccessfull
            return False

        else:
            result.bottom = result_convex.bottom

        # Compute top from bottom and center
        result.top = center.y - (result.bottom - center.y)

    else:
        result.top = result_convex.top

        dist = result_hough.bottom - result_convex.bottom

        if abs(dist) > tolerance:
            # bottom doesn't mach - calculate from top and center
            result.bottom = center.y + (center.y - result.top)

        else:
            result.bottom = result_convex.bottom

    dist = result_hough.left - result_convex.left

    if abs(dist) > tolerance:

        # Left side doesn't match
        dist = result_hough.right - result_convex.right

        if abs(dist) > tolerance:
            # right also doesn't mach - detection unsuccessfull
            return False

        else:
            result.right = result_convex.right

        # Compute left from right and center
        result.left = center.x - (result.right - center.x)

    else:
        result.left = result_convex.left

        dist = result_hough.right - result_convex.right

        if abs(dist) > tolerance:
            # Right side doesn't mach - calculate from top and center
            result.right = center.x + (center.x - result.left)

        else:
            result.right = result_convex.right

    return True
# =====================================================================================================================


# =====================================================================================================================
def symmetrize(center, result, tolerance):

    # symmetrize the result by the center (if off tolerance)
    dist = abs((center.x - result.left) - (result.right - center.x))

    if dist > tolerance:
        bigger = float
        if (center.x - result.left) > (result.right - center.x):
            bigger = (center.x - result.left)

            if abs((center.y - result.top) - bigger) > tolerance and abs((result.bottom - center.y) - bigger) > tolerance:
                result.left = center.x - (result.right - center.x)

        else:
            bigger = (result.right - center.x)

            if abs((center.y - result.top) - bigger) > tolerance and abs((result.bottom - center.y) - bigger) > tolerance:
                result.right = center.x + (center.x - result.left)

    dist = abs((center.y - result.top) - (result.bottom - center.y))

    if dist > tolerance:
        bigger = float

        if (center.y - result.top) > (result.bottom - center.y):
            bigger = (center.y - result.top)

            if abs((center.x - result.left) - bigger) > tolerance and abs((result.right - center.x) - bigger) > tolerance:
                result.top = center.y - (result.bottom - center.y)

        else:
            bigger = (result.bottom - center.y)

            if abs((center.x - result.left) - bigger) > tolerance and abs((result.right - center.x) - bigger) > tolerance:
                result.bottom = center.y + (center.y - result.top)

    return True
# =====================================================================================================================
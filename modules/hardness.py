import cv2
import numpy as np
from config.config import Config
from modules.base import *


# =====================================================================================================================
HV = 0.1
pxsize = 0.1277E-6
# =====================================================================================================================


# =====================================================================================================================
class HardnessResult(object):

    def __init__(self, w=None, h=None, hardness=None):
        self.w = w
        self.h = h
        self.hardness = hardness
# =====================================================================================================================


# =====================================================================================================================
def computeHardness(res: Result) -> HardnessResult:
    dw = res.right - res.left
    dh = res.bottom - res.top

    dw *= pxsize
    dh *= pxsize
    dw *= 1e6
    dh *= 1e6

    F = HV * 9.823

    hardness = 0.1891 * F / (dw * dh)
    hardness *= 1e6

    return HardnessResult(dw, dh, hardness)
# =====================================================================================================================


# =====================================================================================================================
def setLens(magnification):
    pxsize = (0.20432 / (magnification * magnification)) * 1E-3
# =====================================================================================================================
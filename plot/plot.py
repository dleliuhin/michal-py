import cv2
import numpy as np
from config.config import Config
from modules.base import *
from modules.hardness import *


# =====================================================================================================================
def DrawHardness(src, result: Result):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2

    text = "Diagonal1: " + str(round(result.w, 3)) + " um"
    cv2.putText(src, text, (10, 30), font, fontScale, (0, 0, 0), thickness, cv2.LINE_AA)

    text = "Diagonal1: " + str(round(result.h, 3)) + " um"
    cv2.putText(src, text, (10, 70), font, fontScale, (0, 0, 0), thickness, cv2.LINE_AA)

    text = "Hardness: " + str(round(result.hardness, 3)) + " HV"
    cv2.putText(src, text, (10, 110), font, fontScale, (0, 0, 0), thickness, cv2.LINE_AA)
# =====================================================================================================================
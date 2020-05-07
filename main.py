import glob
import cv2
from config.config import Config
from modules.preproces import detect_puncture
from modules.hardness import computeHardness
from plot.plot import *
import numpy as np


# =====================================================================================================================

# Read configuration file
config = Config('./cfg/config.yml')
template = cv2.imread('./dataset/templates/' + config.puncture_tpl_file + '.jpg')

# Read all image filenames from subdirectory
dataset = [[cv2.imread(file), file.replace('./dataset/', '')] for file in glob.glob('./dataset/*.JPG')]

for img, fname in dataset:

    if config.trace:
        print('\n Processing ' + fname)

    img: np.ndarray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, binarized = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if config.trace:
        print('Binarized')

    res, decision = detect_puncture(binarized, template, config)

    hardness = None
    if decision:
        if config.trace:
            print('Puncture detected')

        hardness = computeHardness(res)

        if config.trace:
            print('Hardness computed')

    if config.gui:
        pimg = cv2.resize(img, (300, 250))
        ptmp = cv2.resize(template, (300, 250))
        pgray = cv2.resize(gray, (300, 250))
        pbinarized = cv2.resize(binarized, (300, 250))

        cv2.imshow('input', pimg)
        cv2.moveWindow('input', 0, 0)
        cv2.imshow('template', ptmp)
        cv2.moveWindow('template', 350, 0)
        cv2.imshow('grayscale', pgray)
        cv2.moveWindow('grayscale', 700, 0)
        cv2.imshow('binary', pbinarized)
        cv2.moveWindow('binary', 1050, 0)

    final = img.copy()
    if decision:
        cv2.rectangle(final, (int(res.left), int(res.top)), (int(res.right), int(res.bottom)), (0, 0, 0), 3, 8, 0)
        DrawHardness(final, hardness)

    nfname = './output/final_' + fname
    cv2.imwrite(nfname, final)

    if config.trace:
        print('Image writed as ' + nfname + '\n')

    if config.gui:
        final = cv2.resize(final, (300, 250))
        cv2.imshow('final', final)
        cv2.moveWindow('final', 1050, 700)

    if config.trace:
        cv2.waitKey(0)

    cv2.destroyAllWindows()

if config.trace:
    print('Finish!')

# =====================================================================================================================
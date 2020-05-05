import glob
import cv2
from config.config import Config
from modules.preproces import detect_puncture
import numpy as np

# Read configuration file
config = Config('./cfg/config.yml')
template = cv2.imread('./dataset/templates/' + config.puncture_tpl_file + '.jpg')

# Read all images from subdirectory
dataset = [cv2.imread(file) for file in glob.glob('./dataset/*.JPG')]

# for img in dataset:
# Get first image
img = dataset[0]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, binarized) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

res = detect_puncture(binarized, template, config)

if config.gui:
    pimg = cv2.resize(img, (300, 250))
    ptmp = cv2.resize(template, (300, 250))
    pgray = cv2.resize(gray, (300, 250))
    pbinarized = cv2.resize(binarized, (300, 250))
    # pdenoised = cv2.resize(denoised, (300, 250))

    cv2.imshow('input', pimg)
    cv2.moveWindow('input', 0, 0)
    cv2.imshow('template', ptmp)
    cv2.moveWindow('template', 350, 0)
    cv2.imshow('grayscale', pgray)
    cv2.moveWindow('grayscale', 700, 0)
    cv2.imshow('binary', pbinarized)
    cv2.moveWindow('binary', 1050, 0)
    # cv2.imshow('denoised', pdenoised)
    # cv2.moveWindow('denoised', 1300, 0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

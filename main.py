# =====================================================================================================================
# Authors: Dmitrii Leliuhin
# email: dleliuhin@gmail.com
# =====================================================================================================================

import glob
import cv2
from config.config import Config
from modules.hw_detector import *
from plot.plot import *
import numpy as np

# =====================================================================================================================

# There is example how to parse and process all images in subdirectory
# Read configuration file
config = Config('./cfg/config.yml')
template = cv2.imread('./dataset/templates/' + config.puncture_tpl_file + '.jpg')

# Read all image filenames from subdirectory
dataset = [[cv2.imread(file), file.replace('./dataset/', '')] for file in glob.glob('./dataset/*.JPG')]

# If need process one image. Uncomment two lines under that:
# name = 'MwPic_30_1_2015__16_1__29_407.JPG'
# dataset = [[cv2.imread('./dataset/' + name), name]]

for img, fname in dataset:
    final, d1, d2, hw = hw_detector(img, fname, template, config)

    nfname = './output/final_' + fname
    cv2.imwrite(nfname, final)

    if config.trace:
        print('Image writed as ' + nfname + '\n')

    if config.trace:
        cv2.waitKey(0)

    cv2.destroyAllWindows()

if config.trace:
    print('Finish!')

# =====================================================================================================================
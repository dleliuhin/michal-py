import cv2
import glob

# Read all images from subdirectory
dataset = [cv2.imread(file) for file in glob.glob('./dataset/*.JPG')]

for img in dataset:
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

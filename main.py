import cv2
import glob

# Read all images from subdirectory
dataset = [cv2.imread(file) for file in glob.glob('./dataset/*.JPG')]

# for img in dataset:

# Get first image
img = dataset[0]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, binarized) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

img = cv2.resize(img, (300, 250))
gray = cv2.resize(gray, (300, 250))
binarized = cv2.resize(binarized, (300, 250))

cv2.imshow('input', img)
cv2.moveWindow('input', 0, 0)
cv2.imshow('grayscale', gray)
cv2.moveWindow('grayscale', 350, 0)
cv2.imshow('binary', binarized)
cv2.moveWindow('binary', 700, 0)

cv2.waitKey(0)
cv2.destroyAllWindows()

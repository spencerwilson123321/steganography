import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser("./decode.py")
parser.add_argument("-f", dest="file", required=True)
args = parser.parse_args()
# args.x
# args.y

# 1. Read the file to decode from cmd args.

# img = cv2.imread("white.bmp")
# img_height = len(img)
# img_width = len(img[0])


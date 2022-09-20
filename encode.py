import cv2
import numpy as np

img = cv2.imread("white.bmp")
img_height = len(img)
img_width = len(img[0])

msg = input("Enter a message to hide: ")
msg_in_binary = ''
for char in msg:
    binary = bin(ord(char))[2:]
    if len(binary) != 8:
        binary = '0'*(8-len(binary)) + binary # Padding with leading zeros.
    # print(binary)
    msg_in_binary += binary
# print(msg_in_binary)

# print(int(binary, 2))

def setLSB(x: int) -> None:
    pass

def encode(message, image):
    bin_msg_index = 0
    for y in range(0, img_height):
        for x in range(0, img_width):
            red = image[y, x][0] # R
            green = image[y, x][1] # G
            blue = image[y, x][2] # B
            rb = bin(red)[2:]
            bit = message[bin_msg_index]
            rb = rb[0:7] + bit
            print(rb)
            print(int(rb, 2))
            break
        break

encode(msg_in_binary, img)

# cv2.imwrite("white_changed.bmp", img)
import cv2
import numpy as np

img = cv2.imread("white.bmp")
img_height = len(img)
img_width = len(img[0])

msg = input("Enter a message to hide: ")
binary_msg = ''
for char in msg:
    binary = bin(ord(char))[2:]
    if len(binary) != 8:
        binary = '0'*(8-len(binary)) + binary # Padding with leading zeros.
    # print(binary)
    binary_msg += binary
# print(msg_in_binary)

# print(int(binary, 2))

def setLSB(binary_str: str, x: int) -> None:
    pass

class Done(Exception): pass

def encode(bin_msg, image):
    bin_msg_index = 0
    bin_msg_length = len(bin_msg)
    try:
        for y in range(0, img_height):
            for x in range(0, img_width):
                for colour in image[y, x]:
                    if bin_msg_index >= bin_msg_length:
                        raise Done
                    colour_binary = bin(colour)[2:]
                    bit = bin_msg[bin_msg_index]
                    if len(colour_binary) != 8:
                        colour_binary = '0'*(8-len(colour_binary)) + colour_binary # Padding with leading zeros.
                    colour_binary = colour_binary[0:7] + bit
                    print(colour_binary)
                    bin_msg_index += 1
    except Done:
        pass

encode(binary_msg, img)
cv2.imwrite("stego_image.bmp", img)
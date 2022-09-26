import cv2
import numpy as np
from bitstring import BitArray

class Done(Exception): pass

def create_stego_image(bits: str, cover_image_path: str, output_filename: str, numlsb: int) -> None:
    img = cv2.imread(cover_image_path)
    height, width, depth = img.shape
    print(img.shape)
    index = 0
    try:
        for y in range(0, height):
            for x in range(0, width):
                c_index = 0
                for colour in img[y, x]:
                    if index >= len(bits):
                        raise Done
                    temp = BitArray(uint=colour, length=8)
                    binary_colour = temp.bin
                    data = bits[index:index+numlsb]
                    new_colour = binary_colour[0:(8-numlsb)] + data
                    img[y, x][c_index] = int(new_colour, 2)
                    c_index += 1
                    index += 2
    except Done:
        pass
    # Save the stego image to disk.
    cv2.imwrite(output_filename, img)
    # x = 0
    # while x < len(bits):
    #     data = bits[x:x+numlsb]

    #     x += numlsb


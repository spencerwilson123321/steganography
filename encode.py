from lib2to3.pytree import convert
import cv2
import numpy as np
import argparse
from sys import exit, stderr
from os.path import isfile

# Command Line Arguments
parser = argparse.ArgumentParser("./encode.py")

parser.add_argument("INPUT_FILE_PATH")
parser.add_argument("-o", dest="OUTPUT_FILE_PATH", required=False, default="stego_image.bmp")
args = parser.parse_args()

# Verify inputs
if not isfile(args.INPUT_FILE_PATH):
    print(f"ERROR: Input file '{args.INPUT_FILE_PATH}' not found", file=stderr)
    exit(1)

def int_to_binary(num: int, num_bits: int):
    binary = bin(num)[2:]
    if len(binary) != num_bits:
        binary = "0"*(num_bits-len(binary)) + binary
    return binary

def binary_to_int(binary_number: str):
    return int(binary_number, 2)

class Done(Exception): pass

def encode(bin_msg, image):
    bin_msg_index = 0
    bin_msg_len = len(bin_msg)
    height = len(image)
    width = len(image[0])

    # Encode message size into the first 32 LSBs of the picture.
    # Message size will be stored as a 32 bit integer
    # Unit for message size is BYTES.
    # Therefore, the 32 bit message size integer can represent a message size of up to 4,294,967,296 bytes or 4096 MB
    # which is more than enough space.
    
    # Converting the message length from bytes to binary representation (str).
    msg_len_as_binary = int_to_binary(int(len(bin_msg) / 8), 32) # divide by 8 for bytes.
    # Encode the message length as binary into the first 32 LSBs of the image.
    try:
        y = 0
        index = 0
        for x in range(0, width): # The entire first row of pixels in the image will be reserved for metadata for now.
            colour_index = 0
            for colour in image[y, x]:
                if index >= 32:
                    raise Done
                colour_binary = int_to_binary(colour, 8)
                bit = msg_len_as_binary[index]
                colour_binary = colour_binary[0:7] + bit
                image[y, x][colour_index] = binary_to_int(colour_binary)
                index += 1
                colour_index += 1
    except Done:
        pass

    try:
        for y in range(1, height): # Start at second row to avoid metadata.
            for x in range(0, width):
                colour_index = 0
                for colour in image[y, x]:
                    if bin_msg_index >= bin_msg_len:
                        raise Done
                    colour_binary = int_to_binary(colour, 8)                    # RGB value converted to binary notation (str)
                    bit = bin_msg[bin_msg_index]                                # Get next bit of message using msg index.
                    colour_binary = colour_binary[0:7] + bit                    # Replace the LSB of the RGB value to our message bit.
                    image[y, x][colour_index] = binary_to_int(colour_binary)    # Replace the old RGB value with the encoded RGB value.
                    bin_msg_index += 1
                    colour_index += 1
    except Done:
        pass

if __name__ == "__main__":

    img = cv2.imread(args.INPUT_FILE_PATH)
    msg = input("Enter a message to hide: ")
    binary_msg = ''
    for char in msg:
        binary = bin(ord(char))[2:]
        if len(binary) != 8:
            binary = '0'*(8-len(binary)) + binary # Padding with leading zeros.
        binary_msg += binary

    encode(binary_msg, img)
    cv2.imwrite(args.OUTPUT_FILE_PATH, img)

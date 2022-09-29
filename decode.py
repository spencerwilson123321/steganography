from sys import stderr
from cv2 import imread, imwrite
import numpy as np
import argparse
from os.path import isfile

from image import get_all_bits, get_filename, get_filename_size, get_filesize, get_data

parser = argparse.ArgumentParser("./decode.py")
parser.add_argument("INPUT_FILE_PATH")
parser.add_argument("-n", dest="lsbcount", required=False, default=1, type=int)
args = parser.parse_args()

# Global Variables
header_filesize = 140 # in bytes
header_filename_size = 120 # in bytes

if not isfile(args.INPUT_FILE_PATH):
    print(f"ERROR: File '{args.INPUT_FILE_PATH}' not found.", file=stderr)
    exit(1)

class Done(Exception): pass

if __name__ == "__main__":
    image = imread(args.INPUT_FILE_PATH)
    image = image.flatten() # Easier to deal with image as a linear series of pixel intensities.
    # encrypted_filesize = retrieve_filesize(image, args.lsbcount)
    decoded_bits = get_all_bits(image, args.lsbcount)
    print(len(decoded_bits))
    filesize = get_filesize(decoded_bits)
    print(filesize)
    filename_size = get_filename_size(decoded_bits)
    print(filename_size)
    filename = get_filename(decoded_bits, filename_size)
    filename = "copy" + filename
    data_bytes = get_data(decoded_bits, filename_size, filesize)
    with open(filename, "wb") as f:
        f.write(data_bytes)
    # print(f"Encrypted Filesize: {encrypted_filesize}")
    # encrypted_filename_size = retrieve_filename_size(image, args.lsbcount, offset=140)
    # print(f"Encrypted Filename Size: {encrypted_filename_size}")
    # encrypted_filename = retrieve_filename(image, args.lsbcount, 260, encrypted_filename_size)



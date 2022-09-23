import cv2
import numpy as np
import argparse
from sys import exit, stderr
from encryption import encrypt_bytes, generate_key
from utils import verify_args, check_filesize, read_file_bytes
from bitstring import BitArray
from cryptography.fernet import Fernet

# Command Line Arguments
parser = argparse.ArgumentParser("./encode.py")

parser.add_argument("INPUT_FILE")
parser.add_argument("COVER_IMAGE_FILE")
parser.add_argument("-o", dest="OUTPUT_FILE", required=False, default="stego_image.bmp")
parser.add_argument("-n", dest="lsbcount", required=False, default="1")
args = parser.parse_args()

if __name__ == "__main__":
    
    #  Validate command line inputs. Checks that input files exist and that cover image is of type BMP.
    verify_args(args)

    #  Read bytes from input file.
    file_bytes = read_file_bytes(args.INPUT_FILE)
    if not file_bytes:
        print(f"ERROR: Failed to read any bytes from input file, possibly file empty.")
        exit(1)
    
    #  Generate a secret key if it doesn't exist.
    generate_key()

    #  Create fixed length 64 bit bitstring encrypted header which will store: encrypted input file size and input file name
    # Here is how we do it:
    # Get the encrypted file size and file name.
    # Convert the encrypted file size to a 32 bit bitstring, convert the filename to a 32 bit bitstring.
    # Test to see how big a 64 bit bitstring is when encrypted. This number should be constant I belive.
    # Once we know what the encrypted header size is, then we can read and decrypt it easily. This way the 
    # filesize and filename are hidden.
    # Prepend the encrypted header to the encrypted file bytes.

    #  Encrypt the input file aka creating the ciphertext.
    encrypted_bytes = encrypt_bytes(file_bytes)

    #  Check that the given input file will fit into the cover image.
    if not check_filesize(encrypted_bytes, args.COVER_IMAGE_FILE, int(args.lsbcount)):
        print(f"ERROR: Input file too large to be stored in given cover image.", file=stderr)
        exit(1)
    
    #  Convert the encrypted bytes into bitstring format.

    #  Place encrypted bits into the LSBs of the cover image.


    exit(1)
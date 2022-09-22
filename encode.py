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
    
    # 1. Validate command line inputs. Checks that input files exist and that cover image is of type BMP.
    verify_args(args)

    # 2. Read bytes from input file.
    file_bytes = read_file_bytes(args.INPUT_FILE)
    if not file_bytes:
        print(f"ERROR: Failed to read any bytes from input file, possibly file empty.")
        exit(1)
    
    # 3. Generate a secret key if it doesn't exist.
    generate_key()

    # 4. Create fixed length 64 bit bitstring encrypted header which will store: encrypted input file size and input file name
    # Here is how we do it:
    # Get the encrypted file size and file name.
    # Convert the encrypted file size to a 32 bit bitstring, convert the filename to a 32 bit bitstring.
    # Test to see how big a 64 bit bitstring is when encrypted. This number should be constant I belive.
    # Once we know what the encrypted header size is, then we can read and decrypt it easily. This way the 
    # filesize and filename are hidden.
    # Prepend the encrypted header to the encrypted file bytes.
    # Done.

    # 4. Encrypt the input file aka creating the ciphertext.
    encrypted_bytes = encrypt_bytes(file_bytes)

    # 5. Check that the given input file will fit into the cover image.
    if not check_filesize(encrypted_bytes, args.COVER_IMAGE_FILE, int(args.lsbcount)):
        print(f"ERROR: Input file too large to be stored in given cover image.", file=stderr)
        exit(1)
    
    # 6. Convert the encrypted bytes into bitstring format.

    # 8. Prepend the en

    # 9. Place encrypted bits into the LSBs of the cover image.

    # 8. 

    
    # input_file_bits = ""
    # with open("assignment-01.pdf", 'rb') as input_file:
    #     file_bytes = input_file.read()
    #     for byte_as_int in file_bytes:
    #         byte = BitArray(uint=byte_as_int, length=8)
    #         input_file_bits += byte.bin
    # print(len(input_file_bits))

    exit(1)

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

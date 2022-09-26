import argparse
from sys import exit, stderr
from encryption import encrypt_bytes, generate_key
from image import create_stego_image
from utils import bytes_to_bits, verify_args, check_filesize, read_file_bytes, get_filename, create_header_encrypted

# Command Line Arguments
parser = argparse.ArgumentParser("./encode.py")

parser.add_argument("INPUT_FILE")
parser.add_argument("COVER_IMAGE_FILE")
parser.add_argument("-o", dest="OUTPUT_FILE", required=False, default="stego_image.bmp")
parser.add_argument("-n", dest="lsbcount", required=False, default="1", type=int)
args = parser.parse_args()

if __name__ == "__main__":

    # Header Format: 32 bit encrypted filesize (140 bytes) | 16 bit encrypted filename size (100 bytes) | filename size bits of encrypted filename
    # Data: filesize bits of encrypted data
    # 140 bytes for filesize, 120 bytes for filename size 
    
    #  Validate command line inputs. Checks that input files exist and that cover image is of type BMP.
    verify_args(args)

    #  Read bytes from input file.
    file_bytes = read_file_bytes(args.INPUT_FILE)
    if not file_bytes:
        print(f"ERROR: Failed to read any bytes from input file, possibly file empty.")
        exit(1)
    
    #  Generate a secret key if it doesn't exist.
    generate_key()

    #  Encrypt the input file aka creating the ciphertext.
    encrypted_bytes = encrypt_bytes(file_bytes)

    #  Check that the given input file will fit into the cover image.
    if not check_filesize(encrypted_bytes, args.COVER_IMAGE_FILE, int(args.lsbcount)):
        print(f"ERROR: Input file too large to be stored in given cover image.", file=stderr)
        exit(1)

    # Get filename, convert to bytes, and encrypt.    
    filename = get_filename(args.INPUT_FILE)
    filename_bytes = bytes(filename, encoding="utf-8")
    filename_bytes_encrypted = encrypt_bytes(filename_bytes)

    # Get the encrypted filename size.
    encrypted_filename_size = len(filename_bytes_encrypted)
    
    # Get the encrypted filesize.
    encrypted_filesize = len(encrypted_bytes)

    # Create the encrypted metadata header using filesize, filename size, and filename.
    encrypted_header_bytes = create_header_encrypted(encrypted_filesize, encrypted_filename_size, filename_bytes_encrypted)

    # Convert the encrypted file bytes into bitstring format.
    file_bits = bytes_to_bits(encrypted_bytes)

    # Convert the encrypted header bytes into bitstring format.
    header_bits = bytes_to_bits(encrypted_header_bytes)

    # Place the data bits into the cover image.
    bits = header_bits + file_bits
    create_stego_image(bits, args.COVER_IMAGE_FILE, args.OUTPUT_FILE, args.lsbcount)

    exit(1)

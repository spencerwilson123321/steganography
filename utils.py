from os.path import isfile, split
from os import stat
from sys import exit, stderr
from bitstring import BitArray
from encryption import encrypt_bytes

def verify_file_path(path: str) -> bool:
    if not isfile(path):
        return False
    return True

def get_extension_from_path(path: str) -> str:
    tokens = path.split("/")
    tokens = tokens[len(tokens)-1].split(".")
    if len(tokens) == 1:
        return ""
    extension = tokens[1]
    return extension

def check_bmp_file(path: str) -> bool:
    extension = get_extension_from_path(path)
    if not extension:
        print(f'ERROR: Cannot parse extension from path "{path}"')
        exit(1)
    if extension != "bmp":
        return False
    return True

def verify_args(args):
    if not verify_file_path(args.INPUT_FILE):
        print(f"ERROR: Input file '{args.INPUT_FILE}' not found", file=stderr)
        exit(1)
    if not verify_file_path(args.COVER_IMAGE_FILE):
        print(f"ERROR: Cover image file '{args.COVER_IMAGE_FILE}' not found", file=stderr)
        exit(1)
    if not check_bmp_file(args.COVER_IMAGE_FILE):
        print(f"ERROR: Bad cover image file extension '{args.COVER_IMAGE_FILE}' only .bmp files are supported. ", file=stderr)
        exit(1)

# def check_filesize(input_path: str, cover_path: str, lsbcount: int) -> bool:
#     input_stats = stat(input_path)
#     cover_stats = stat(cover_path)
#     # Calculate max number of bytes the cover image can store with the given lsbcount
#     max_bytes = (cover_stats.st_size * lsbcount) / 8 
#     print(f"Input file size: {input_stats.st_size} Bytes")
#     print(f"Cover image size: {cover_stats.st_size} Bytes")
#     print(f"Max input file size: {max_bytes} Bytes")
#     if input_stats.st_size >= max_bytes:
#         return False
#     return True

def check_filesize(input_bytes: bytes, cover_path: str, lsbcount: int) -> bool:
    cover_stats = stat(cover_path)
    # Calculate max number of bytes the cover image can store with the given lsbcount
    max_bytes = ((cover_stats.st_size * lsbcount) / 8) - 1000 # -1000 to reserve space for header.
    print(f"Encrypted input file size: {len(input_bytes)} Bytes")
    print(f"Cover image size: {cover_stats.st_size} Bytes")
    print(f"Max input file size: {max_bytes} Bytes")
    if len(input_bytes) >= max_bytes:
        return False
    return True

def read_file_bytes(path: str) -> bytes:
    bytes = b''
    with open(path, "rb") as f:
        bytes = f.read()
    return bytes

def get_filename(path: str) -> str:
    head, tail = split(path)
    return tail

def get_filesize_in_bytes(path: str) -> int:
    stats = stat(path)
    return int(stats.st_size)

def create_header_encrypted(encrypted_filesize: int, filename_encrypted_size: int, filename_encrypted_bytes: bytes) -> bytes:
    # Take enc filesize and convert to BitArray 32 bit string, and then encrypt the 32 bit string.
    binary_encrypted_filesize = BitArray(uint=encrypted_filesize, length=32)
    filesize_encrypted_bytes = encrypt_bytes(bytes(binary_encrypted_filesize.bin, encoding="utf-8"))
    print(f"Filesize encrypted bytes length: {len(filesize_encrypted_bytes)}")
    
    # filename size
    binary_filename_size = BitArray(uint=filename_encrypted_size, length=16)
    filename_size_encrypted_bytes = encrypt_bytes(bytes(binary_filename_size.bin, encoding="utf-8"))
    print(f"Filename size encrypted bytes length: {len(filename_size_encrypted_bytes)}")

    return filesize_encrypted_bytes + filename_size_encrypted_bytes + filename_encrypted_bytes

def bytes_to_bits(data: bytes) -> str:
    bits = ""
    for x in data:
        byte = BitArray(uint=x, length=8)
        bits += byte.bin
    return bits
# def convert_int_to_binary(num: int) -> str:
#     binary = bin(num)[2:]
#     if len(binary) != num_bits:
#         binary = "0"*(num_bits-len(binary)) + binary
#     return binary
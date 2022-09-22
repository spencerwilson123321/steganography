from os.path import isfile
from os import stat
from sys import exit, stderr

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
    max_bytes = (cover_stats.st_size * lsbcount) / 8 
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

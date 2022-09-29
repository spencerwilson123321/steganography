import cv2
import numpy as np
from bitstring import BitArray
from encryption import decrypt_bytes

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

def get_all_bits(image, lsbcount) -> str:
    decoded_bits = ""
    for i in range(0, len(image)):
        number = image[i]
        bits = BitArray(uint=number, length=8)
        decoded_bits += bits.bin[len(bits)-lsbcount:]
    return decoded_bits

def convert_bitstring_to_bytes(bits: str):
    data = ""
    index = 0
    while index+8 <= len(bits):
        data += chr(int(bits[index:index+8], 2))
        index += 8
    return bytes(data, encoding='utf-8')

def get_filesize(decoded_bits: str) -> int:
    # We know the filesize is stored in the first 140 bytes.
    # 140 * 8 = 1120 bits.
    filesize = 0
    filesize_bits = decoded_bits[0:1120]
    filesize_bytes = convert_bitstring_to_bytes(filesize_bits)
    filesize_decrypted = decrypt_bytes(filesize_bytes)
    filesize = int(filesize_decrypted.decode("utf-8"), 2)
    return filesize

def get_filename_size(decoded_bits: str) -> int:
    # Filename size is stored in 120 bytes.
    # 120 * 8 = 960
    filename_size = 0
    filename_bits = decoded_bits[1120:1120+960]
    filename_bytes = convert_bitstring_to_bytes(filename_bits)
    filename_decrypted = decrypt_bytes(filename_bytes)
    filename_size = int(filename_decrypted.decode("utf-8"), 2)
    return filename_size

def get_filename(decoded_bits: str, filename_size: int) -> str:
    filename_bits = decoded_bits[2080:2080+(filename_size*8)]
    filename_bytes = convert_bitstring_to_bytes(filename_bits)
    filename_decrypted = decrypt_bytes(filename_bytes)
    return filename_decrypted.decode("utf-8")

def get_data(decoded_bits: str, filename_size: int, filesize: int):
    data_bits = decoded_bits[2080+(filename_size*8):2080+(filename_size*8)+(filesize*8)]
    data_bytes = convert_bitstring_to_bytes(data_bits)
    decrypted_bytes = decrypt_bytes(data_bytes)
    return decrypted_bytes

# def retrieve_filesize(image, lsbcount: int):
#     # The filesize is always encoded as 140 bytes at the start of the file.
#     # 140*8 = 1120 bits for the encrypted file size.
#     number_of_pixel_intensities_to_count = int(1120/lsbcount)
#     decoded_bits = ""
#     for i in range(0, number_of_pixel_intensities_to_count):
#         number = image[i]
#         bits = BitArray(uint=number, length=8)
#         decoded_bits += bits.bin[len(bits)-lsbcount:]
#     # Turn the decoded bits into the string characters they actually represent
#     # and then convert to bytes, and then decrypt.
#     original = ""
#     pointer = 0
#     while pointer+8 <= 1120:
#         original += chr(int(decoded_bits[pointer:pointer+8], 2))
#         pointer += 8
#     decrypted_bytes = decrypt_bytes(bytes(original, encoding="utf-8"))
#     # Now convert the decrypted bytes back to string, and convert
#     # it to it's original number.
#     encrypted_filesize = int(decrypted_bytes.decode("utf-8"), 2)
#     return encrypted_filesize

def retrieve_filename_size(image, lsbcount, offset) -> int:
    # 120 bytes for the filename size.
    # 120 * 8 = 960 bits
    decoded_bits = ""
    pixel_intensities_to_skip = int((offset*8)/lsbcount)
    for i in range(pixel_intensities_to_skip, 960+pixel_intensities_to_skip):
        number = image[i]
        bits = BitArray(uint=number, length=8)
        decoded_bits += bits.bin[len(bits)-lsbcount:]
    original = ""
    pointer = 0
    while pointer+8 <= 1120:
        original += chr(int(decoded_bits[pointer:pointer+8], 2))
        pointer += 8
    decrypted_bytes = decrypt_bytes(bytes(original, encoding="utf-8"))
    encrypted_filename_size = int(decrypted_bytes.decode(("utf-8")), 2)
    return encrypted_filename_size

def retrieve_filename(image, lsbcount, offset: int, filename_size: int) -> str:
    decoded_bits = ""
    print(filename_size)
    pixel_intensities_to_skip = int((offset*8)/lsbcount)
    filename_size = int((filename_size*8)/lsbcount)
    print(pixel_intensities_to_skip)
    print(filename_size)
    for i in range(pixel_intensities_to_skip, filename_size+pixel_intensities_to_skip):
        number = image[i]
        bits = BitArray(uint=number, length=8)
        decoded_bits += bits.bin[len(bits)-lsbcount:]
    original = ""
    print(len(decoded_bits))
    pointer = 0
    while pointer+8 <= filename_size:
        original += chr(int(decoded_bits[pointer:pointer+8], 2))
        pointer += 8
    print(original)
    # decrypted_bytes = decrypt_bytes(bytes(original, encoding="utf-8"))
    # filename = decrypted_bytes.decode(("utf-8"))
    # print(filename)
    filename = ""
    return filename





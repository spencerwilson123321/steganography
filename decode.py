from sys import stderr
from cv2 import imread, imwrite
import numpy as np
import argparse
from os.path import isfile

parser = argparse.ArgumentParser("./decode.py")
parser.add_argument("INPUT_FILE_PATH")
args = parser.parse_args()

if not isfile(args.INPUT_FILE_PATH):
    print(f"ERROR: File '{args.INPUT_FILE_PATH}' not found.", file=stderr)
    exit(1)


class Done(Exception): pass


class Bits():

    def __init__(self, value: str or int, numBits: int):
        self.__bits = ""
        if type(value) is str:
            temp = bin(ord(value))[2:]
            if len(temp) != numBits:
                temp = "0"*(numBits-len(temp)) + temp
            self.__bits = temp
        elif type(value) is int:
            temp = bin(value)[2:]
            if len(temp) != numBits:
                temp = "0"*(numBits-len(temp)) + temp
            self.__bits = temp
        elif type(value) is np.uint8:
            temp = bin(value)[2:]
            if len(temp) != numBits:
                temp = "0"*(numBits-len(temp)) + temp
            self.__bits = temp
        self.__len = numBits
    
    def __getitem__(self, key):
        return self.__bits[key]
    
    def __repr__(self):
        return self.__bits

    def setLSB(bits: str) -> None:
        pass

    def getLSB() -> str:
        pass

    def getBits(start, end):
        pass

    def getBit(index):
        pass

    def toInt() -> int:
        pass

    def toString() -> str:
        pass


class EncodedImage:

    def __init__(self):
        self.__imgMatrix = None
        self.__numColourChannels = 0
        self.__numPixels = 0
        self.__width = 0
        self.__height = 0
    
    def loadImage(self, file_path):
        self.__imgMatrix = imread(file_path)
        self.__numColourChannels = self.__imgMatrix.shape[2]
        self.__width = self.__imgMatrix.shape[1]
        self.__height = self.__imgMatrix.shape[0]
        self.__numPixels = self.__width * self.__height

    def saveImage(self, file_path):
        imwrite(file_path, self.__imgMatrix)
    
    def getPixel(self, y, x):
        return self.__imgMatrix[y, x]
    
    def setPixel(self, y, x, pixel):
        self.__imgMatrix[y, x] = pixel
    
    def getPixelRow(self, y):
        return self.__imgMatrix[y]

    def getHeight(self):
        return self.__height
    
    def getWidth(self):
        return self.__width

    def getNumColourChannels(self):
        return self.__numColourChannels

    def getNumPixels(self):
        return self.__numPixels

    def getColourChannel(self, pixel, colour: str):
        if colour == "red":
            return pixel[0]
        elif colour == "green":
            return pixel[1]
        elif colour == "blue":
            return pixel[2]


class Decoder:

    def __init__(self):
        pass

    def decodeMessageSize(self, img: EncodedImage):
        msg_size = 0
        # Do something
        msg_size_decoded = ""
        try:
            for x in range(0, img.getWidth()):
                pixel = img.getPixel(0, x)
                for colour in ["red", "green", "blue"]:
                    if len(msg_size_decoded) == 32:
                        raise Done
                    colour_intensity = img.getColourChannel(pixel, colour)
                    bits = Bits(colour_intensity, 8)
                    encoded_bit = bits[7]
                    msg_size_decoded += encoded_bit
        except Done:
            pass
        msg_size = int(msg_size_decoded, 2)
        return msg_size

    def decodeMessage(self, img: EncodedImage, msg_size: int):
        # Do something
        message_bits = ""
        decoded_message = ""
        try:
            for y in range(1, img.getHeight()):
                for x in range(0, img.getWidth()):
                    pixel = img.getPixel(y, x)
                    for colour in ["red", "green", "blue"]:
                        if len(message_bits) == msg_size*8:
                            raise Done
                        colour_intensity = img.getColourChannel(pixel, colour)
                        bits = Bits(colour_intensity, 8)
                        encoded_bit = bits[7]
                        message_bits += encoded_bit
        except Done:
            pass
        print(f"Decoded Message in Binary: {message_bits}")
        for x in range(0, msg_size*8, 8):
            bits = message_bits[x:x+8]
            decoded_message += chr(int(bits, 2))
        return decoded_message


if __name__ == "__main__":
    image = EncodedImage()
    decoder = Decoder()
    image.loadImage(args.INPUT_FILE_PATH)
    msg_size = decoder.decodeMessageSize(image)
    message = decoder.decodeMessage(image, msg_size)
    print(f'Decoded Message Size: {msg_size} Bytes')
    print(f'Decoded Message: "{message}"')
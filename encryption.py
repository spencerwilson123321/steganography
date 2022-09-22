from cryptography.fernet import Fernet
from os.path import isfile
from sys import stderr

def encrypt_bytes(file_bytes: bytes) -> bytes:
    encrypted_bytes = b''
    key = read_key()
    if not key:
        print(f"ERROR: Key file empty or unable to read bytes.", file=stderr)
        exit(1)
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(file_bytes)
    return encrypted_bytes

def generate_key() -> None:
    if not isfile("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as keyfile:
            keyfile.write(key)

def read_key() -> bytes:
    key = b''
    if not isfile("secret.key"):
        return b''
    with open("secret.key", "rb") as keyfile:
        key = keyfile.read()
    return key
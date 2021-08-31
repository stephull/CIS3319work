'''
    cipher.py   -- Functions for encryption and decryption
'''

from configurations import *
from string import *
import random as r

# inherit all ascii values for key generation
all_values = ascii_letters + digits + punctuation

# generate key for both client + server to use
def generate_key():
    str = ""
    length = r.choice(range(MIN_KEY_LEN, MAX_KEY_LEN))
    for i in range(length):
        str += r.choice(all_values)
    return str

# generate to ciphertext OR encrypt message
def encrypt_text(resource):
    pass

# recieve plaintext from ciphertext OR decrypt server/client msg.
def decrypt_text(resource):
    pass

'''
    :::EXAMPLE:::
    key is: {generate_key()}
    Sent plaintext is: [normal words]
    Sent ciphertext is: {encrypt_text()}
'''
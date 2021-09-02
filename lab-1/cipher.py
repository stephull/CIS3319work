'''
    cipher.py   -- Functions for encryption and decryption
'''

from configurations import *

# inherit all ascii values for key generation
all_values = string.ascii_letters + string.digits + string.punctuation

# assemble new text file for key
def generate_keyfile(resource):
    new_path = f"{KEYFILE}" if os.getcwd() == str(DIRECTORY) else f"{DIRECTORY}/{KEYFILE}"
    p = open(new_path, 'w')
    p.write(resource)
    p.close()
    return new_path

# generate key for both client + server to use
def generate_key(n):
    str = ""
    for i in range(n):
        str += random.choice(all_values)
    return str

# generate to ciphertext OR encrypt message
def encrypt_msg(key, text):
    return DesKey(str.encode(key)).encrypt(str.encode(text), initial=0, padding=True)

# recieve plaintext from ciphertext OR decrypt server/client msg.
def decrypt_msg(resource):
    return resource
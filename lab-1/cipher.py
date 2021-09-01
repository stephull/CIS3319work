'''
    cipher.py   -- Functions for encryption and decryption
'''

from configurations import *

# inherit all ascii values for key generation
all_values = string.ascii_letters + string.digits + string.punctuation

# assemble new text file for key
def generate_keyfile(resource):
    new_path = "{}/{}".format(DIRECTORY, KEYFILE)
    f = open(new_path, 'w')
    f.write(resource)
    f.close()
    return new_path

# convert list to string type (may be duplicate of generate_key())
def listToString(resource):
    str = ""
    for i in resource:
        str += i
    return str

# generate key for both client + server to use
def generate_key():
    str = ""
    for i in range(random.choice(range(MIN_KEY_LEN, MAX_KEY_LEN))):
        str += random.choice(all_values)
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
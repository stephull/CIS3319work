'''
    gears.py   -- Functions for encryption and decryption
'''

from configurations import *

# inherit all ascii values for key generation
all_values = string.ascii_letters + string.digits + string.punctuation

# assemble new text file for key AND generate key for both client + server to use
def generate_keyfile(resource):
    new_path = f"{KEYFILE}" if os.getcwd() == str(DIRECTORY) else f"{DIRECTORY}/{KEYFILE}"
    with open(new_path, 'w') as p:
        p.write(resource)
        p.close()
    return new_path
def generate_key(n):
    str = ""
    for i in range(n):  str += random.choice(all_values)
    return str
keyfile = generate_keyfile(generate_key(KEY_LEN))

# format messages each time an output is made
def format_msg(key, input, output, mode):
    print(FORMAT_STR)
    if mode == ENC:
        print(f'\tKEY: {key}')
        print(f'\tSent plaintext: {input}')
        print(f'\tSent ciphertext: {output}')
    else:
        print(f'\tSent ciphertext: {input}')
        print(f'\tSent plaintext: {output}')
    print(FORMAT_STR)

# DesKey generation for each time a request from client or server is made
def make_key():
    with open(keyfile, 'r') as k:
        key = k.read()
        k.close()
    return key
key = make_key()

# generate to ciphertext OR encrypt message
def encrypt_msg(key, text):
    temp = DesKey(str(key).encode())
    return temp.encrypt(str(text).encode(), initial=0, padding=True)

# recieve plaintext from ciphertext OR decrypt server/client msg.
def decrypt_msg(key, value):
    try:
        temp = DesKey(str(key).encode())
        return temp.decrypt(str(value).encode(), initial=0, padding=True)
    except:
        return False
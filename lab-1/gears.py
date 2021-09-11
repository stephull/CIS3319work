'''
    gears.py   -- Functions for encryption and decryption
'''

from configurations import *

# inherit all ascii values for key generation
all_values = string.ascii_letters + string.digits

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

# make DesKey for encryption and decryption 
def make_key():
    key = None
    with open(keyfile, "r") as k:
        key = k.read().strip()
        k.close()
    return key

# generate to ciphertext OR back to plaintext
def encrypt_msg(new_deskey, input):
    k = des("DESCRYPT", CBC, new_deskey, pad=None, padmode=PAD_PKCS5)
    return k.encrypt(input)
def decrypt_msg(new_deskey, value):
    try:
        d = des("DESCRYPT", CBC, new_deskey, pad=None, padmode=PAD_PKCS5)
        return d.decrypt(value) 
    except:
        return False
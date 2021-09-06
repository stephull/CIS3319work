'''
    gears.py   -- Functions for encryption and decryption
'''

from configurations import *

# inherit all ascii values for key generation
all_values = string.ascii_letters + string.digits #+ string.punctuation

# assemble new text file for key
def generate_keyfile(resource):
    new_path = f"{KEYFILE}" if os.getcwd() == str(DIRECTORY) else f"{DIRECTORY}/{KEYFILE}"
    with open(new_path, 'w') as p:
        p.write(resource)
        p.close()
    return new_path

# generate key for both client + server to use
def generate_key(n):
    str = ""
    for i in range(random.choice(n)):
        str += random.choice(all_values)
    return str

# assemble key file for both server and client to share
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

# generate to ciphertext OR encrypt message
def encrypt_msg(key, text):
    #return "ENCRYPT TEST: {}, {}".format(text, key).encode('utf-8')
    return DesKey(str.encode(key)).encrypt(str.encode(text), initial=0, padding=True)

# recieve plaintext from ciphertext OR decrypt server/client msg.
def decrypt_msg(key, value):
    #return "DECRYPT TEST: {}, {}".format(value, key).encode('utf-8')
    print("TEST KEY: ", value)
    return DesKey(str.encode(key)).decrypt(str.encode(value), initial=0, padding=True)
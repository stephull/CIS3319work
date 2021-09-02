'''
    main.py     -- Main program for project
'''

from configurations import *
from cipher import *
from server import *
from client import *

# first function, make sure all ports are within respective range
def check_port(n):
    return n if n <= MAX_PORT and n >= MIN_PORT else -1

# main method
def main():
    # check if port is valid
    if (check_port(PORT) < 0):
        raise ValueError(f'\n\n :: PORT invalid, change to value between {MIN_PORT} and {MAX_PORT} :: \n')
    print(f'PORT {PORT} valid')

    # connect client and server into main program
    #server_side()

    # input
    print("Enter your message (8, 16, or 24 characters long) >>> ", end=" ")
    plaintext = str(input())        # must be 8, 16, or 24 characters long
    assert len(plaintext) in (8, 16, 24)

    # generate key file with the assembled key
    keyfile = generate_keyfile(generate_key(KEY_LEN))

    # try
    with open(keyfile, "r") as k:

        # ciphertext
        key_text = k.read()
        temp_key = DesKey(str.encode(key_text))
        temp_key.encrypt(str.encode(plaintext))

        k.close()

# start program
if __name__ == "__main__":
    main()
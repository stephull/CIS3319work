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

    # generate key file with the assembled key
    keyfile = generate_keyfile(generate_key(KEY_LEN))

    # connect client and server into main program
    #server_side()
    #client_side()

    '''
    TEST FOR NOW...
    '''

    # input
    print("Enter your message >>> ", end=" ")
    plaintext = str(input())        
        # QUESTION: WHY DOES IT WORK ONLY ON 8, 16, 24 char.s long?

    # format everything into one place :-)
    def format_msg():
        print(FORMAT_STR)
        print(f'\tKEY: {x}')
        print(f'\tSent plaintext: {plaintext}')
        print(f'\tSent ciphertext: {ciphertext}')
        print(FORMAT_STR)

    # try
    with open(keyfile, "r") as k:
        x = k.read()
        ciphertext = encrypt_msg(x, plaintext)
            # NEXT TIME: find a way to convert each byte into ASCII values
            #   example output now: b'\xc6\xa3k2er8\x98'
            #   we want something like AGfuwrocwu0y328qc51t2v or whatever
        format_msg()

        k.close()

# start program
if __name__ == "__main__":
    main()
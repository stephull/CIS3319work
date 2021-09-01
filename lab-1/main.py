'''
    main.py     -- Main program for project
'''

from configurations import *
from cipher import *
#from server import *
#from client import *

# first function, make sure all ports are within respective range
def check_port(n):
    return n if n <= MAX_PORT and n >= MIN_PORT else -1

# main method
def main():
    # check if port is valid
    if (check_port(PORT) < 0):
        raise ValueError('\n\n :: PORT invalid, change to value between {} and {} :: \n'.format(MIN_PORT, MAX_PORT))
    print('PORT {} valid'.format(PORT))

    # input
    print("Enter your message:", end=" ")
    plaintext = str(input())

    # generate key file with the assembled key
    keyfile = generate_keyfile(generate_key())

    # print contents to console
    print("\n :: TEST, NOT REAL :: ")
    print("Generated key is: ", open(keyfile, "r").read())
    print("Sent plaintext is: ", plaintext)
    print("TEST Sent ciphertext is: {}".format(listToString(random.sample(all_values, len(plaintext)))))
    print('\n')

# start program
if __name__ == "__main__":
    main()
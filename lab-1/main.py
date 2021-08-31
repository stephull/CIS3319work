'''
    main.py     -- Main program for project
'''

from configurations import *
from cipher import *
from server import *
from client import *

def check_port(n):
    return n if n <= MAX_PORT and n >= MIN_PORT else -1

def generate_keyfile(resource):
    new_path = "{}/{}".format(DIRECTORY, KEYFILE)
    f = open(new_path, 'w')

    # will overwrite any existing contents if file already exists:
    f.write(resource)
    f.close()

# main method
def main():
    # check if port is valid
    if (check_port(PORT) < 0):
        raise ValueError('\n\n :: PORT invalid, change to value between {} and {} :: \n'.format(MIN_PORT, MAX_PORT))
    print('PORT {} valid'.format(PORT))

    # generate key file with the assembled key
    generate_keyfile(generate_key())

    # call server + client:
    #start_server()
    #start_client()

# start program
if __name__ == "__main__":
    main()
# configurations.py
# file to hold all constants and enumerated values, for all files
# AND contains all functionalities for executing methods (gears).

'''
    imports
'''
from hashlib import *       # main import for HMAC and hashing functionalities
from pyDes import *         # for encryption of messages transmitted between server and client
from socket import *        # for socket programming functionalities
import random, os, sys, string

'''
    constants and finals 
'''
# current working directory information
CWD = "lab-2"
FULL_CWD = f"C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}"

# text files
HMAC = "HMAC.txt"
DES = "DES.txt"

# arguments
ENC = 0, DEC = 1
SERVER = "server"
CLIENT = "client"

# for socket programming localhost and port
PORT = 8008
HOST = "127.0.0.1"
PORT_MIN = 1024
PORT_MAX = 49151

# for socket programming interior methods or variables
BACKLOG = 1
RECV_BYTES = 1024
INPUT_STR = "ENTER MESSAGE>>> "
EXIT_KEY = "-1"

# lengths of string literals
KEY_LEN = 8
ARGS_LEN = 2
HASH_LEN = 64

# arguments count
FORMAT_ARGV_MIN = 4
FORMAT_ARGV_MAX = 5

# size of variables in SHA-1
BLOCK_SIZE = 64
OUTPUT_SIZE = 20

# other important things
OPAD = "36"
IPAD = "5c"

'''
    functions
'''
# generate key AND file for either HMAC or DES
def make_keyfile(file):
    new_path = f"{file}" if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{file}"
    resource = ""
    values = string.ascii_letters + string.digits + string.punctuation
    for i in range(KEY_LEN) : resource += random.choice(values)
    with open(new_path, "w") as k:
        k.write(resource)
        k.close()
    return new_path
HMAC_keyfile = make_keyfile(HMAC)
DES_keyfile = make_keyfile(DES)

'''
    FYI: the 4 functions below are for theoretical purposes :-)
    check back on HMAC encryption algorithm and 5/26/22 on my planner.
    --> HMAC(K,M) = H[(K' XOR opad) || H[(K' XOR ipad) || M ] ]
                    H[] = hash()
                    K' = pad_key(key)
                    K' XOR #### = XOR_contents(####)
                    K' XOR #### || M = concatentate_with_msg()
    ALSO, it's very possible that this stuff is already in the libraries
'''
# function for implementing hash function
def hash():
    pass

# use padding for key 
def pad_key(key):
    if key > BLOCK_SIZE:
        pass
    pass

# use the padded key and either opad/ipad to XOR
def XOR_contents():
    pass

# concatenate, for instance, the result of XOR and the message bitstring
def concatenate_with_msg():
    pass

#####

# convert message into encrypted DES key
def create_DESkey():
    pass

# encrypt or decrypt messages, use DES key as mentioned above
def descrypt(mode):
    pass

# verify, once received, that both received and newly calculated HMAC are the same
def verify_HMAC(received, calculated):
    return True if received == calculated else False

# for formatting message each time a message is sent or if one is received
def format_msg(other_party, recv=False, *argv):
    assert len(argv) == FORMAT_ARGV_MAX if recv else len(argv) == FORMAT_ARGV_MIN

    # if recv is True, it means the message has been both sent and recieved
    # other indicates a party that is opposite from the person sending or receiving
    fluff=":::::"
    msg = "Sending to: " if recv else "Sent from: "
    header = f"{fluff}{msg}{other_party}{fluff}"

    print(header)
    if (recv):
        # this is the receiving side
        print(f"Received ciphertext: {argv[0]}")
        print(f"Received message: {argv[1]}")
        r = argv[2], c = argv[3]
        print(f"Recevied HMAC: {r}")
        print(f"Calculated HMAC: {c}")
        print(f"HMAC verified: {verify_HMAC(r, c)}")
    else:
        # this is the sender's side
        print(f"Shared DES key: {argv[0]}")
        print(f"Shared HMAC key: {argv[1]}")
        print(f"Plain message: {argv[2]}")
        print(f"Sender side HMAC: {argv[3]}")
        print(f"Sent ciphertext: {argv[4]}")
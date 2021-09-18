# configurations.py
# file to hold all constants and enumerated values, for all files
# AND contains all functionalities for executing methods (gears).

'''
    imports
'''
import hashlib          # main import for hashing functionalities
import hmac             # main import for HMAC functionalities
import pyDes            # for encryption of messages transmitted between server and client
from socket import *        # for socket programming functionalities
import random, os, sys, string      # for other important methods...

'''
    constants and finals 
'''
# current working directory information
CWD = "lab-2"
FULL_CWD = f"C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}"

# text files
HMAC_FILE = "HMAC.txt"
DES_FILE = "DES.txt"

# arguments
ENC = 0
DEC = 1
SERVER = "server"
CLIENT = "client"

# for socket programming
PORT = 8008
HOST = "127.0.0.1"
PORT_MIN = 1024
PORT_MAX = 49151
BACKLOG = 1
RECV_BYTES = 1024
INPUT_STR = "ENTER MESSAGE >>> "
EXIT_KEY = "-1"

# lengths of string literals
DES_KEY_LEN = 8
HMAC_KEY_LEN = 16
ARGS_LEN = 2
HASH_LEN = 64

# arguments count
FORMAT_ARGV_MIN = 4
FORMAT_ARGV_MAX = 5

# size of variables in SHA-256
BLOCK_SIZE = 64
OUTPUT_SIZE = 20

'''
    functions
'''
# generate key AND file for either HMAC or DES
def make_keyfile(file):
    new_path = f"{file}" if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{file}"
    values = string.ascii_letters + string.digits + string.punctuation
    assert file == DES_FILE or file == HMAC_FILE
    key_length = DES_KEY_LEN if (file == DES_FILE) else HMAC_KEY_LEN

    resource = ""
    for i in range(key_length) : resource += random.choice(values)
    with open(new_path, "w") as k:
        k.write(resource)
        k.close()
    return new_path
HMAC_keyfile = make_keyfile(HMAC_FILE)
DES_keyfile = make_keyfile(DES_FILE)

'''
    FYI: the 4 functions below are for theoretical purposes :-)
    check back on HMAC encryption algorithm and 5/26/22 on my planner.
    --> HMAC(K,M) = H[(K' XOR opad) || H[(K' XOR ipad) || M ] ]
'''
# function for implementing hash function
def hash(msg):
    return hashlib.sha256(str.encode(msg)).hexdigest()
    # QUESTION: is this necessary, or is get_hmac enough?!?

# function that returns the construction of the HMAC
def get_hmac(key, input):
    sha = hmac.new(str.encode(key), digestmod=hashlib.sha256)
    sha.update(str.encode(input))
    return sha.hexdigest()

# convert message into encrypted DES key
def create_DESkey(key):
    return pyDes.des(key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5)

# for concatentation of message and HMAC before DES
def concat(msg, hash):
    return str.encode(msg) + str.encode(hash)

# encrypt or decrypt messages, use DES key as mentioned above, use ENC or DEC
def descrypt(mode, key, input):
    assert mode == ENC or mode == DEC
    try: return create_DESkey(key).encrypt(input) if mode == ENC else create_DESkey(key).decrypt(input)
    except: return False

# verify, once received, that both received and newly calculated HMAC are the same
def verify_HMAC(received, calculated):
    return True if received == calculated else False

# for formatting message each time a message is sent or if one is received
def format_msg(recv, *argv):
    assert len(argv) == FORMAT_ARGV_MIN if recv else FORMAT_ARGV_MAX

    # if recv is True, it means the message has been both sent and recieved
    # other indicates a party that is opposite from the person sending or receiving
    fluff=" ::::: "
    msg = "Receiver side" if recv else "Sender side"
    header = f"{fluff}{msg}{fluff}"

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
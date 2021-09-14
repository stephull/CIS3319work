# configurations.py
# file to hold all constants and enumerated values, for all files
# AND contains all functionalities for executing methods (gears).

'''
    imports
'''
from hashlib import *       # main import for HMAC and hashing functionalities
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
ENC = 0
DEC = 1
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
INPUT_STR = "Send message >>> "
EXIT_KEY = "-1"

# lengths of string literals
KEY_LENGTH = 0
ARGS_LENGTH = 2

'''
    functions
'''

# generate key AND file for either HMAC or DES
def make_keyfile(file):
    new_path = f"{file}" if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{file}"
    resource = None
    values = string.ascii_letters + string.digits
    
    with open(new_path, "w") as k:
        k.write(resource)
        k.close()

# convert message data to HMAC
def convert_to_HMAC():
    pass

# concatenate string with DES key
def concatenate_with_DES():
    pass

# verify, once received, that both received and newly calculated HMAC are the same
def verify_HMAC():
    pass

# for formatting message each time a message is sent or if one is received
def format_msg(other, recv=False):
    # if recv is True, it means the message has been both sent and recieved
    # other indicates a party that is opposite from the person sending or receiving
    fluff=":::::"
    msg = "Sending to: " if recv else "Sent from: "
    header = f"{fluff}{msg}{other}{fluff}"

    print(header)
    if (recv):
        # this is the receiving side
        print("Received ciphertext: {}")
        print("Received message: {}")
        print("Recevied HMAC: {}")
        print("Calculated HMAC: {}")
        print("HMAC verified") if verify_HMAC() == True else print("Couldn't verify HMAC")
    else:
        # this is the sender's side
        print("Shared DES key: {}")
        print("Shared HMAC key: {}")
        print("Plain message: {}")
        print("Sender side HMAC: {}")
        print("Sent ciphertext: {}")

'''
    Configurations.py
    ::: Handles all essential definitions of functions, imports, and constant values :::
'''

'''
    Imports
'''
from pyDes import *
from socket import *
import string, random
import os, sys
import time, calendar

'''
    Constants
'''
CWD = "lab-5"
FULL_CWD = f'C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}'

# arguments for execution
CLIENT = "client"
ASTGS = "authentication"
SERVPRO = "service"

# arguments for cryptography (encryption/decryption)
ENC = 0
DEC = 1

# ID codes
ID_CLIENT = "CIS3319USERID"
ID_ASTGS = "CIS3319TGSID"
ID_SERVPRO = "CIS3319SERVERID"

# fixed length values
ARGS_LEN = 2

# generated key files
FORMAT_TXT = ".txt"
DIR_KEYS = "Keys"
KEY_CLIENT = "key-client"
KEY_ASTGS = "key-astgs"
KEY_SERVPRO = "key-servpro"

# socket programming configurations
PORT = 8387
LOCALHOST = "127.0.0.1"
NET_ADDR = f'{LOCALHOST}:{str(PORT)}'
PORT_MIN = 1024
PORT_MAX = 49151
BACKLOG = 2

# time functions
LIFETIME2 = 60
LIFETIME4 = 8.64e4


'''
    Functions
'''
# create key files in advance, before program starts
def make_keyfile(file):
    assert file == KEY_CLIENT or KEY_ASTGS or KEY_SERVPRO
    new_path = f'{DIR_KEYS}/{file}{FORMAT_TXT}' if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{DIR_KEYS}/{file}{FORMAT_TXT}"
    values = string.ascii_letters + string.digits + string.punctuation
    keylen = 8  ### for now
    resource = "".join(random.sample(values, keylen))
    with open(new_path, "w") as k:
        k.write(resource)
        k.close()
    return new_path

# read key from key file
def read_key(file):
    with open(file, "r") as a:
        key = a.read().strip()
        a.close()
    return key

# declare new keyfiles
keyfile_CLIENT = make_keyfile(KEY_CLIENT)
keyfile_ASTGS = make_keyfile(KEY_ASTGS)
keyfile_SERVPRO = make_keyfile(KEY_SERVPRO)

# create timestamp using UNIX time
def make_ts():
    timestruct = time.gmtime()
    return calendar.timegm(timestruct)

# concatentate messages and contents
def concat(*args):
    resource = ""
    for i in args: resource += args[i]
    return resource

def split_contents(resource, n):
    # n indicates how many items to return
    pass

# use DES to encrypt and decrypt contents
def make_DES(key):
    return des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
def descrypt(mode, key, value):
    assert mode == ENC or DEC
    try: return make_DES(key).encrypt(value) if mode == ENC else make_DES(key).decrypt(value, padmode=PAD_PKCS5)
    except: return False
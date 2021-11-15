'''
    Configurations.py : configure imports, functions, and final variables
'''

'''
    Imports 
'''
import pyDes, math
import threading as th
import string as st
import random as r
import calendar as ca
import os, sys, time
from socket import *


'''
    Constant values 
'''
CWD = "lab-6"
FULL_CWD = f'C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}'

ENC = 0
DEC = 1
CLIENT = "client"
SERVER = "server"
CA = "ca"

ARGS_LEN = 2
TS_LEN = 10
KEY_LEN = 8
PRIME_LIM = 4
PRIME_LOG = 3

TXT = ".txt"
DIR_KEYS = "Keys/"
CA_PUB_KEY = f"{DIR_KEYS}ca_public_key{TXT}" #PK(ca)
S_PUB_KEY = f"{DIR_KEYS}s_public_key{TXT}"   #PK(s)
RSA_PUB_KEY = f"{DIR_KEYS}rsa_public_key{TXT}"
DES_SESS_KEY = f"{DIR_KEYS}des_sess_key{TXT}"
TEMP1_KEY = f"{DIR_KEYS}temp1_key{TXT}"
TEMP2_KEY = f"{DIR_KEYS}temp2_key{TXT}"

ID_CA = "ID-CA"
ID_C = "ID-client"
ID_S = "ID-server"
REQ = "memorandum"
DATA = "take cis3319 class this morning"
LT_SESS = 8.64e4

PORT = 8088
HOST = "127.0.0.1"
PORT_LIM = range(1024, 49151+1)
RECV_BYTES = 1024
BACKLOG = 2
EXIT_KEY = '-1'
SLEEP_LOG = 0.1

INPUT_STR = ">>> "
ERROR_MSG_PRIME = "\nERROR: primality test calculates out of bounds\n"
PO = [[
        "1. Ciphertext and generated K(tmp1)", # S
        "1. Ciphertext and received K(tmp1)"  # CA 
    ], [
        "2. Ciphertext, generated key pair, and Cert(s) generated",     # CA
        "2. Ciphertext, received key pair, and Cert(s) received"       # S
    ], [
        "3. Plaintext", "4. Plaintext" # both sides
    ], [
        "5. Ciphertext, generated K(tmp2)", # C
        "5. Ciphertext, received K(tmp2)"  # S 
    ], [
        "6. Ciphertext, generated K(sess)",  # S
        "6. Ciphertext, received K(sess)"   # C
    ], [
        "7. Ciphertext, receieved req message", # on S side
        "8. Ciphertext, received data message"
    ]       # PO[][], PO[2] and PO[5] are unique.
]


'''
    Functions
'''
# check for directory of project
def check_dir(e) : return f"{FULL_CWD}/{e}" if os.getcwd() != str(FULL_CWD) else e

# generate key through files or by themselves
def stream_key():
    val = st.digits+st.ascii_letters+st.punctuation
    return "".join(r.sample(val, KEY_LEN))
def write_key(e, content=None):
    path = check_dir(e)
    with open(path, "w") as k: 
        if content==None : k.write(stream_key())
        else : k.write(content)
        k.close()
    return path
def read_key(e):
    with open(check_dir(e), "r") as a: 
        k = a.read().strip(); a.close()
    return k

# generate key files for program use
ca_pub_keyfile = write_key(CA_PUB_KEY)
s_pub_keyfile = write_key(S_PUB_KEY)
temp1_des_keyfile = write_key(TEMP1_KEY)
temp2_des_keyfile = write_key(TEMP2_KEY)

# make timestamp
def ts() : return ca.timegm(time.gmtime())

# concatenate and split contents
def concat(*args):
    ret = ""
    for a in args: ret += a
    return ret
def split(e):
    pass

# DES encryption
def make_des(k) : return pyDes.des(k, pyDes.CBC, k, pad=None, padmode=pyDes.PAD_PKCS5)
def descrypt(mod, k, e):
    return make_des(k).encrypt(e) if mod==ENC else make_des(k).decrypt(e, padmode=pyDes.PAD_PKCS5)

# print contents onto console
def console_log(n, *args):
    fluff = ":"*64; p = ""
    for a in args : p += (a+'\n')
    print(f'\n{fluff}', PO[n], p, '{fluff}\n')
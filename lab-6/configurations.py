'''
    Configurations.py : configure imports, functions, and final variables
'''

'''
    Imports 
'''
import pyDes, math
import hashlib, hmac
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
ABC_LEN = 26
MD5_LEN = 32

TXT = ".txt"
DIR_KEYS = "Keys/"
CA_PUB_KEY = f"{DIR_KEYS}ca_public_key{TXT}" #PK(ca)
S_PUB_KEY = f"{DIR_KEYS}s_public_key{TXT}"   #PK(s)
RSA_PUB_KEY = f"{DIR_KEYS}rsa_public_key{TXT}"
DES_SESS_KEY = f"{DIR_KEYS}des_sess_key{TXT}"

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
JUNK = "//"
ERROR_MSG_PRIME = "\nERROR: primality test calculates out of bounds\n"
PO = [[
        "\n::::: 1. Ciphertext and generated K(tmp1)", # S
        "\n::::: 1. Ciphertext and received K(tmp1)"  # CA 
    ], [
        "\n::::: 2. Ciphertext, generated key pair, and Cert(s) generated",     # CA
        "\n::::: 2. Ciphertext, received key pair, and Cert(s) received"       # S
    ], [
        "\n::::: 3. Plaintext", 
        "\n::::: 4. Plaintext" # for both sides
    ], [
        "\n::::: 5. Ciphertext, generated K(tmp2)", # C
        "\n::::: 5. Ciphertext, received K(tmp2)"  # S 
    ], [
        "\n::::: 6. Ciphertext, generated K(sess)",  # S
        "\n::::: 6. Ciphertext, received K(sess)"   # C
    ], [
        "\n::::: 7. Ciphertext, receieved req message", # on S side
        "\n::::: 8. Ciphertext, received data message"
    ]       # PO[][], PO[2] and PO[5] are unique.
]


'''
    Functions
'''
# check for directory of project
def check_dir(e) : return f"{FULL_CWD}/{e}" if os.getcwd() != str(FULL_CWD) else e

# generate key through files or by themselves
def stream_key() : return "".join(r.sample(st.digits+st.ascii_letters+st.punctuation, KEY_LEN))
def write_key(e, *args):
    path = check_dir(e)
    with open(path, "w") as k: 
        k.write("".join(a+'\n' for a in args)) if len(args) > 0 else k.write(stream_key())
        k.close()
    return path
def read_key(e, rsa=False):
    with open(check_dir(e), "r") as a: 
        if rsa is False : k = a.read().strip()
        else:
            k = []
            for l in a.readlines() : k.append(int(l.strip()))
        a.close()
    return k
write_key(CA_PUB_KEY)
write_key(S_PUB_KEY)

# concatenate contents for messages and make timestamp
def ts() : return ca.timegm(time.gmtime())
def concat(*args) : return "".join(i for i in args)

# splitting methods for specific exchanges
def s_ca_split(e): 
    a = len(e)-TS_LEN
    return e[:KEY_LEN], e[KEY_LEN:a]
def ca_s_split(e):
    a = 2*KEY_LEN; b = a + MD5_LEN
    return e[:KEY_LEN], e[KEY_LEN:a], e[a:b]

# DES encryption
def make_des(k) : return pyDes.des(k, pyDes.CBC, k, pad=None, padmode=pyDes.PAD_PKCS5)
def descrypt(mod, k, e):
    return make_des(k).encrypt(e) if mod==ENC else make_des(k).decrypt(e, padmode=pyDes.PAD_PKCS5)

# print contents onto console
def console_log(n, *args):
    fluff = ":"*64
    print(f'\n{fluff}', PO[n], "".join(a+'\n' for a in args), '{fluff}\n')
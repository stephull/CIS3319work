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

ARGS_LEN = 3
TS_LEN = 10
KEY_LEN = 8
PRIME_LEN = 3

TXT = ".txt"
DIR_KEYS = "Keys"

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

INPUT_STR = ">>> "
PO = {
    "1. Ciphertext and generated K(tmp1)", # S
    "1. Ciphertext and received K(tmp1)",  # CA
    "2. Ciphertext, generated key pair, and Cert(s) generated",     # CA
    "2. Ciphertext, received key pair, and Cert(s) received",       # S
    "3. Plaintext", # both sides
    "4. Plaintext", # both sides
    "5. Ciphertext, generated K(tmp2)", # C
    "5. Ciphertext, received K(tmp2)",  # S
    "6. Ciphertext, generated K(sess)",  # S
    "6. Ciphertext, received K(sess)",   # C
    "7. Ciphertext, receieved req message", # on S side
    "8. Ciphertext, received data message"
        # 12 total messages, 8 steps (1,2,5,6 double)
}


'''
    Functions
'''
# check for directory of project
def check_dir(e): 
    return f"{FULL_CWD}/{e}" if os.getcwd() != str(FULL_CWD) else e

# generate key through files or by themselves
def stream_key():
    val = st.digits+st.ascii_letters+st.punctuation
    return "".join(r.sample(val, KEY_LEN))

# make key files and read for local usage
def write_key(e):
    path = check_dir(e)
    with open(path, "w") as k : k.write(stream_key()); k.close()
    return path
def read_key(e):
    with open(check_dir(e), "r") as a : k = a.read().strip(); a.close()
    return k

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
def make_des(k, e) : return pyDes.des(k, pyDes.CBC, k, pad=None, padmode=pyDes.PAD_PKCS5)
def descrypt(mod, k, e):
    return make_des(k).encrypt(e) if mod==ENC else make_des(k).decrypt(e, padmode=pyDes.PAD_PKCS5)

# AKS primality test forgenerating p and q in RSA
c = [0] * math.pow(10, PRIME_LEN)
def primality_test(n):
    c[0] = 1
    for i in range(n):
        c[i+1] = 1
        for j in range(i, 0, -1):
            c[j] = c[j-1] - c[j]
        c[0] = -c[0]
    c[0] += 1
    c[n] -= 1
    i = n
    while (i > -1 and c[i] % n == 0) : i -= 1
    return True if i < 0 else False

# use RSA encryption
def rsa_signature(e):
    pass
def rsacrypt(mod, k, e):
    assert mod==ENC or mod==DEC
    # more info here: https://www.pythonpool.com/rsa-encryption-python/
    
    if (mod == ENC):
        
        return
    else:
        
        return

# print contents onto console
def console_log(n, *args):
    fluff = ":"*64; p = ""
    for a in args : p += (a+'\n')
    print(f'\n{fluff}', PO[n], p, '{fluff}\n')
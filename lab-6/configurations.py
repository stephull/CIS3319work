import pyDes
import math
from socket import *
import string, random
import os, sys
import time, calendar

'''
    Constant values 
'''

CWD = "lab-6"
FULL_CWD = f'C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}'

ENC = 0
DEC = 1

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

'''
    Functions
'''
# check for directory of project
def check_dir(e):
    pass

# make key files and read for local usage
def write_key(e):
    pass
def read_key(e):
    pass

# make timestamp
def ts():
    pass

# concatenate and split contents
def concat(*args):
    pass
def split(e):
    pass

# DES encryption
def make_des(k, e):
    pass
def descrypt(mod, k, e):
    pass

# use RSA encryption (including possible primality test for prime numbers)
def primality_test(n):
    pass
def rsacrypt(mod, k, e):
    # more info here: https://www.pythonpool.com/rsa-encryption-python/
    pass

# print contents onto console
def console_log(e, *args):
    pass
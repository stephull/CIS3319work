'''
    configurations.py   -- Includes all constants for all files
'''

import random, string       # for randomization and ASCII values
import sys, os, errno       # for system and OS operations, error recognition, and terminal execution
sys.path.append(r'c:/users/shull/appdata/local/packages/pythonsoftwarefoundation.python.3.7_qbz5n2kfra8p0/localcache/local-packages/python37/site-packages')
from des import DesKey      # outside import: for DES algorithm

# important attributes or variables
PORT = 3319
LOCALHOST = "127.0.0.1"

BACKLOG = 2
RECV_BYTES = 1024

INPUT_LENGTH = 64
MAX_PORT = 49151
MIN_PORT = 1024

DIRECTORY = "C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/lab-1"
KEYFILE = "key.txt"
KEY_LEN = 8

INPUT_STR = "Type message >>> "
FORMAT_STR = '=' * 40
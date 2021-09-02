'''
    configurations.py   -- Includes all constants for all files
'''

# imports are for ALL files (include path for external imports)
import sys, os, errno
sys.path.append(r'c:/users/shull/appdata/local/packages/pythonsoftwarefoundation.python.3.7_qbz5n2kfra8p0/localcache/local-packages/python37/site-packages')

import random, string
from des import DesKey

# important attributes or variables
PORT = 6666
LOCALHOST = "127.0.0.1"

BACKLOG = 2
RECV_BYTES = 1024

INPUT_LENGTH = 64
MAX_PORT = 49151
MIN_PORT = 1024

DIRECTORY = "lab-1"
KEYFILE = "key.txt"
KEY_LEN = 8

INPUT_STR = "Type message >>> "
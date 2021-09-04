'''
    configurations.py   -- Includes all constants for all files
'''

import random, string       # for randomization and ASCII values
import sys, os, errno       # for system and OS operations, error recognition, and terminal execution
from socket import *        # for socket programming essentials

sys.path.append(r'c:/users/shull/appdata/local/packages/pythonsoftwarefoundation.python.3.7_qbz5n2kfra8p0/localcache/local-packages/python37/site-packages')
from des import DesKey      # outside import: for DES algorithm

# essential properties for chat program
PORT = 3319
LOCALHOST = "127.0.0.1"

# for backlog and number of bytes socket can receive
BACKLOG = 2
RECV_BYTES = 1024

# length of input
INPUT_LENGTH = 64
ARGS_LENGTH = 2
KEY_LEN = (8, 16, 24)

# for port number range
MAX_PORT = 49151
MIN_PORT = 1024

# files/directories
DIRECTORY = "C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/lab-1"
KEYFILE = "key.txt"

# for arguments, command line 
ARGS_HELP = ['<program exe>', '<client OR server>']
COMM = sys.argv[1]
CLIENT = "client"
SERVER = "server"

# for formatting messages while chat program is running
INPUT_STR = "\nType message >>> "
FORMAT_STR = '=' * 72

# for formatting messages based on whether operation is encryption or decryption
ENC = 0
DEC = 1

# for exiting program altogether
EXIT_KEY = -1
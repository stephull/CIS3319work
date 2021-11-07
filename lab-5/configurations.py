'''
    Configurations.py
    ::: Handles all essential definitions of functions, imports, and constant values :::
'''

'''
    Imports
'''
import pyDes
from _thread import *
from socket import *
import string, random, os, sys, time, calendar

'''
    Constants
'''
CWD = "lab-5"
FULL_CWD = f'C:/Users/shull/OneDrive/Desktop/School/FALL 2021/CIS 3319/CIS3319work/CIS3319work/{CWD}'

# arguments for execution
CLIENT = "client"
AUTH = "auth"
SERV = "serv"

# arguments for cryptography (encryption/decryption)
ENC = 0
DEC = 1

# ID codes
ID_CLIENT = "CIS3319USERID"
ID_AUTH = "CIS3319TGSID"
ID_SERV = "CIS3319SERVERID"

# fixed length values
ARGS_LEN = 2
ARGS_LIMITS = range(2,5)    #?
KEY_LEN = 8
TS_LEN = 10

# generated key files
TXT = ".txt"
DIR_KEYS = "Keys"
KEY_CLIENT = f"{DIR_KEYS}/key-{CLIENT}{TXT}"
KEY_AUTH = f"{DIR_KEYS}/key-{AUTH}{TXT}"
KEY_SERV = f"{DIR_KEYS}/key-{SERV}{TXT}"

# IMPORTANT: deleted Results, sticking to print msg's only.

# socket programming configurations
HOST = '127.0.0.1'
PORT = 8888
PORT_LIMITS = range(1024, 49151+1)
BACKLOG = 2
RECV_BYTES = 1024
EXIT_KEY = "-1"

# time functions
LIFETIME2 = 60
LIFETIME4 = int(8.64e4)

# other stuff
INPUT_STR = ">>> "

# not constants, but still needed here : printouts for all messages for lab
po = [
    "1. Received messages, C -> AS:\n", 
    "2. Plaintext of recieved ciphertext, AS -> C:\n",
    "3. Received message and Ticket(tgs) validity:\n", 
    "4. Plaintext of received ciphertext, TGS -> C:\n",
    "5. Received message and Ticket(v) validity:\n", 
    "6. Plaintext of received ciphertext, V -> C:\n"
]

'''
    Functions + other important variables
'''
# create key files in advance, before program starts 
# + double-check for correct redirection in project files
def check_dir(e) : return e if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{e}"
def make_keyfile(e):
    new_path = check_dir(e)
    values = string.ascii_letters + string.digits + string.punctuation
    resource = "".join(random.sample(values, KEY_LEN))
    with open(new_path, "w") as k:
        k.write(resource)
        k.close()
    return new_path

# read key from key file
def read_key(file):
    with open(check_dir(file), "r") as a:
        key = a.read().strip()
        a.close()
    return key

# declare new keyfiles
keyfile_CLIENT = make_keyfile(KEY_CLIENT)
keyfile_AUTH = make_keyfile(KEY_AUTH)
keyfile_SERV = make_keyfile(KEY_SERV)

# create timestamp (seconds) using UNIX time
def ts():
    timestruct = time.gmtime()
    return calendar.timegm(timestruct)

# concatentate messages and contents
def concat(*args):
    ret = ""
    for a in args: ret += str(a)
    return ret

# for any exchange, confirm that values are correct:
def confirm_c_to_as(resource):
    ret1 = str(resource[:len(ID_CLIENT)])
    ret2 = str(resource[len(ID_CLIENT):len(ID_CLIENT + ID_AUTH)])
    ret3 = str(resource[len(ID_CLIENT + ID_AUTH):])
    assert ret1 == ID_CLIENT and ret2 == ID_AUTH, "Client ID and/or TGS ID do not match accordingly"
    return [ret1, ret2, ret3]
def split_as_to_c(resource, key, *args):
    newstr = ""
    newlen = 0
    for a in args: 
        if type(a) == str : newstr += a
        elif type(a) == int : newlen += a
    temp = resource[newlen+len(newstr)-1:]
    temp.replace("\"", '\'')
    return temp

# to create authenticators
def make_authenticator(key, *args):
    #timestamps will be created here and passed back
    return

# use DES to encrypt and decrypt contents
def make_DES(key) : return pyDes.des(key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5)
def descrypt(mode, key, value):
    try: return make_DES(key).encrypt(value) if mode == ENC else make_DES(key).decrypt(value, padmode=pyDes.PAD_PKCS5)
    except: return False

# format message
def format_print(n, e):
    fluff = ':'*64
    print(f"\n{fluff}\n", po[n], e, f"\n{fluff}\n")
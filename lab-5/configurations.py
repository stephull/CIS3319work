'''
    Configurations.py
    ::: Handles all essential definitions of functions, imports, and constant values :::
'''

'''
    Imports
'''
import pyDes
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
SERVER = "server"
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

# generate Results
DIR_RET = "Results"
RET_1 = f"{DIR_RET}/results-{AUTH}{TXT}"
RET_2 = f"{DIR_RET}/results-{SERV}{TXT}"

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

temp = "\n>>> Log:    Start "
input_id_client = "Enter the client ID: \n"
input_id_auth = "Enter the TGS access ID (for auth. server): \n"
input_id_serv = "Enter the service provider ID: \n"
ticket_c_as = "Confirm ticket to proceed to TGS: \n"
key_c_as = "Enter key given to proceed to TGS: \n"
ticket_c_v = "Confirm ticket to proceed to service provider: \n"
key_c_v = "Enter key given to proceed to service provider: \n"

'''
    Functions + other important variables
'''
# does the input allow for program to continue running?
def check_send(conn, e):
    if str(e).lower().strip() != EXIT_KEY : return True
    conn.send(str.encode(EXIT_KEY))
    return False

# generate key using string ASCII values
# + double-check for correct redirection in project files
def check_dir(e) : return e if os.getcwd() == str(FULL_CWD) else f"{FULL_CWD}/{e}"
def stream_key():
    values = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(values, KEY_LEN))

# create key files 
def make_keyfile(e):
    path = check_dir(e)
    with open(path, "w") as k:
        k.write(stream_key())
        k.close()
    return path

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
def split_c_to_v(resource):
    for i in range(len(resource)):
        if resource[i] == 'b' and (resource[i+1] == "\'" or "\""):
            return resource[0:i].strip()
    return resource.strip()

# print results to Results file
def write_to_results(e, t, k):
    with open(check_dir(e), "w") as op:
        op.write(t)
        op.write('\n')
        op.write(k)
        op.close()

# to create authenticators
def make_authenticator(key, id, t) : return descrypt(ENC, key, id+str(t))

# use DES to encrypt and decrypt contents
def make_DES(key) : return pyDes.des(key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5)
def descrypt(mode, key, value):
    try: return make_DES(key).encrypt(value) if mode == ENC else make_DES(key).decrypt(value, padmode=pyDes.PAD_PKCS5)
    except: return False

# format message
def format_print(n, *args):
    fluff = ':'*64
    e = ""
    for a in args : e += (a + "\n")
    print(f"\n{fluff}\n", po[n], e, f"\n{fluff}\n")
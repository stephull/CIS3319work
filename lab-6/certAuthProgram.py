'''
    For certificate authority program
'''
# includes public key PK(ca), private key SK(ca)

from configurations import *
from rsa_functions import *

def certAuthProgram():
    print("Starting certificate authority program...")
    ca_socket = socket(AF_INET, SOCK_STREAM)
    ca_socket.connect((HOST, PORT))
    
    # send input
    ca_msg = input(INPUT_STR)
    
    while ca_msg.lower().strip() != EXIT_KEY:
        
        # RECV first exchange: S -> CA
        # >> RSA(PKca) [K(tmp1) || ID(s) || TS1], K(tmp1) generates on S
        
        # SEND second exchange: CA -> S
        # >> DES(Ktmp1) [PK(s) || SK(s) || Cert(s)|| ID(s) || TS2]
        # >> >> Cert(s) = Sign(SKca) [ID(s) || ID(ca) || PK(s)]
        # >> >> Sign(SKca) is RSA signature generation with specified private key
        
        # fin
        break
    
    ca_socket.close()
    sys.exit()
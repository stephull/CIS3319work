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
    while True:
        # get public and private key
        local_ca_pub_key = read_key(CA_PUB_KEY)
        local_ca_pri_key = stream_key()
        
        # RECV first exchange: S -> CA        
        rsa_priv_d_value = int(ca_socket.recv(RECV_BYTES).decode())
        rsa_priv_n_value = int(ca_socket.recv(RECV_BYTES).decode())
        ca_socket.send(JUNK.encode())   # (to reduce chances of overloading socket send direction at once)
        rsa_crypted_value = eval(ca_socket.recv(RECV_BYTES).decode())
        compared_value = ca_socket.recv(RECV_BYTES).decode()
        
        decrypted_rsa_ca = rsacrypt(DEC, rsa_priv_n_value, rsa_priv_d_value, rsa_crypted_value)     #  P <-- C^d mod n
        returned_rsa_str = digitize_text(DEC, decrypted_rsa_ca)
        assert returned_rsa_str == compared_value, "RSA Error: RSA decryption failed to correctly return valid string"
        
        print('yippee:', returned_rsa_str)
        
        # SEND second exchange: CA -> S
        # >> DES(Ktmp1) [PK(s) || SK(s) || Cert(s)|| ID(s) || TS2]
        # >> >> Cert(s) = Sign(SKca) [ID(s) || ID(ca) || PK(s)]
        # >> >> Sign(SKca) is RSA signature generation with specified private key
        
        # fin
        break
    
    ca_socket.close()
    sys.exit()
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
        begin_ca = ca_socket.recv(RECV_BYTES).decode()
        if (begin_ca == JUNK):
            priv_s_rsa_key = begin_rsa()    # for RSA private key
            pub_rsa_key = read_key(RSA_PUB_KEY, True)   # returns n and e, respectively
            pub_rsa_n = pub_rsa_key[0]; pub_rsa_e = pub_rsa_key[1]
            ca_socket.send(str(pub_rsa_key).encode())
        else: 
            print("Invalid connection. Open client using python3 main.py client")
            break
            
        # get public and private key
        pri_rsa_n = priv_s_rsa_key[1]; pri_rsa_d = priv_s_rsa_key[0]
        local_ca_pub_key = read_key(CA_PUB_KEY)     # PKca
        imported_s_pub_key = read_key(S_PUB_KEY)    # PKs
        local_ca_pri_key = stream_key()     # SKca
        
        # RECV first exchange: S -> CA        
        rsa_crypted_value = eval(ca_socket.recv(RECV_BYTES).decode())   # main
        ca_socket.send(JUNK.encode())
        decrypted_rsa_ca = rsacrypt(pri_rsa_n, pri_rsa_d, rsa_crypted_value)     #  P <-- C^d mod n
        returned_rsa_str = digitize_text(DEC, decrypted_rsa_ca)
        assert returned_rsa_str == ca_socket.recv(RECV_BYTES).decode(), "RSA Error: RSA decryption failed to correctly return valid string"
        
        # PRINTOUT 1
        returned_s_key, returned_s_id = s_ca_split(returned_rsa_str)
        print(PO[0][1])
        print(rsa_crypted_value)
        print(returned_s_key, '\n\n')
        
        # SEND second exchange: CA -> S
        # >> DES(Ktmp1) [PK(s) || SK(s) || Cert(s) || ID(s) || TS2]
        
        # More info on cert: https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/digital-signatures/rsa-sign-verify-examples.html
        new_cert = create_rsa_sign(local_ca_pri_key, pub_rsa_n, pub_rsa_e, concat(
            returned_s_id, ID_CA, imported_s_pub_key
        ))
        priv_s_key = stream_key()       # SKs
        des_key = descrypt(ENC, returned_s_key, concat(
            imported_s_pub_key, priv_s_key, new_cert, returned_s_id, str(ts())
        ))
        ca_socket.send(des_key)
        
        # PRINTOUT 2
        print(PO[1][0])
        print(des_key)
        print([imported_s_pub_key, priv_s_key])
        print(new_cert, '\n\n')
        
        # Exit out of socket, terminate CA program.
        time.sleep(1)
        print("\nThank you for using the certificate authenticator.")
        print(f"Redirect to the client using the same commands: \tpython3 main.py <{CLIENT}>")
        print(f"\n{EXIT_MSG}{CA}\n\n")
        break
    
    ca_socket.close()
    sys.exit()
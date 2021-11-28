'''
    Client program
'''

from configurations import *
from rsa_functions import *

def clientProgram():
    print("Starting client program...")
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.connect((HOST, PORT))

    while True:
        print("\nConnected to client program...\n")
        assert c_socket.recv(RECV_BYTES).decode() == INTERMEDIATE_PASS, "Error: invalid connection for client-server exchange.\n"
        c_socket.send(str(JUNK).encode())
        
        # SEND third exchange: C -> S
        # >> ID(s) || TS3
        c_s_1_ts = str(ts())
        c_s_1_concat = concat(ID_S, c_s_1_ts)
        c_socket.send(str.encode(c_s_1_concat))
        
        # PRINTOUT 3
        print(PO[2][0])
        print(ID_S, c_s_1_ts, '\n\n')
        
        # RECV fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        s_c_recv = c_socket.recv(RECV_BYTES).decode()
        s_pub_key, cert, returned_ts = s_c_1_split(s_c_recv)
        
        # PRINTOUT 4
        print(PO[2][1])
        print(s_pub_key, cert, returned_ts, '\n\n')
        
        # verify the contents of vertificate first
        validate_cert = c_socket.recv(RECV_BYTES).decode()
        c_socket.send(JUNK.encode())
        s_pub_key = eval(c_socket.recv(RECV_BYTES).decode())
        c_socket.send(JUNK.encode())
        cert = eval(c_socket.recv(RECV_BYTES).decode())
        decrypted_rsa_cert = rsacrypt(s_pub_key[0], s_pub_key[1], cert)
        returned_cert_str = digitize_text(DEC, decrypted_rsa_cert)
        if (validate_cert == returned_cert_str):
            print("\nCertificate valid: continue\n")
        else:
            print("\nCertificate Invalid: RSA decryption failed to correctly return valid string\n")
            break   
        
        # SEND fifth exchange: C -> S
        # >> RSA(PKs) [K(tmp2) || ID(c) || IP(c) || Port(c) || TS5], generate K(tmp2)
        # before we move on, we must verify S's public key and certificate
        ktmp2 = stream_key()
        c_s_2_ts = str(ts())
        client_rsa_pub_key = eval(c_socket.recv(RECV_BYTES).decode())
        c_s_2_concat = concat(ktmp2, ID_C, HOST, PORT, c_s_2_ts)
        c_s_2_digits = digitize_text(ENC, c_s_2_concat)
        s5_send = rsacrypt(client_rsa_pub_key[0], client_rsa_pub_key[1], c_s_2_digits)
        c_socket.send(str(s5_send).encode())    # main
        c_socket.recv(RECV_BYTES)
        c_socket.send(str(c_s_2_concat).encode())
        
        # PRINTOUT 5
        print(PO[3][0])
        print(s5_send)
        print(ktmp2, '\n\n')
        
        # RECV sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]
        s6_recv = c_socket.recv(RECV_BYTES)
        returned_s6_data = descrypt(DEC, ktmp2, s6_recv).decode()
        new_sess_key, returned_lt, returned_s6_ts = s_c_2_split(returned_s6_data)
        
        # PRINTOUT 6
        print(PO[4][1])
        print(s6_recv)
        print(new_sess_key, '\n\n')
        
        # SEND seventh exchange: C -> S
        # >> DES(Ksess) [req || TS7]
        s7_ts = str(ts())
        s7_send = descrypt(ENC, new_sess_key, concat(REQ, s7_ts))
        c_socket.send(s7_send)
        
        # PRINTOUT 7
        print(PO[5][0])
        print(s7_send)
        print('\nMessage:\t', REQ, '\n\n')
        
        # RECV eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        s8_recv = c_socket.recv(RECV_BYTES)
        returned_s8_data = descrypt(DEC, new_sess_key, s8_recv).decode()
        returned_data_val, returned_s8_ts = s_c_3_split(returned_s8_data)
        
        # PRINTOUT 8
        print(PO[5][1])
        print(s8_recv)
        print('\nFinal message: \t', returned_data_val, '\n\n')
        
        # fin 
        break
    
    c_socket.close()
    sys.exit()
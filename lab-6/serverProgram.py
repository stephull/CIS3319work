'''
    Server program: for server
'''

from configurations import *
from rsa_functions import *

# for any exchange between the server and certificate authenticator
def serverProgram():
    print("Starting server program...")
    s_socket = socket(AF_INET, SOCK_STREAM)
    s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s_socket.bind((HOST, PORT))
    s_socket.listen(BACKLOG)
    
    while True:
        conn, addr = s_socket.accept()
        if conn: 
            print("\nUPDATE: Connected to client...\n")
            conn.send(JUNK.encode())
            pub_rsa_key = eval(conn.recv(RECV_BYTES).decode())
        
        # SEND first exchange: S -> CA
        # >> RSA(PKca) [K(tmp1) || ID(s) || TS1], K(tmp1) generates on S
        local_key_temp1 = stream_key()
        exchange1_contents = concat(local_key_temp1, ID_S, str(ts()))
        exchange1_digits = digitize_text(ENC, exchange1_contents)
        s1_send_msg = rsacrypt(pub_rsa_key[0], pub_rsa_key[1], exchange1_digits)   # P^e mod n --> C
                
        # https://www.geeksforgeeks.org/python-interconvert-tuple-to-byte-integer/
        conn.send(str(s1_send_msg).encode())    # main
        conn.recv(RECV_BYTES)
        conn.send(str(exchange1_contents).encode())
        
        # PRINTOUT 1
        print(PO[0][0])
        print(s1_send_msg)
        print(local_key_temp1, '\n\n')
        
        # RECV second exchange: CA -> S
        returned_des_key = conn.recv(RECV_BYTES)
        conn.send(JUNK.encode())
        returned_des_contents = descrypt(DEC, local_key_temp1, returned_des_key).decode()   
        
        global validate_cert, ca_s_pub_key, cert       # for future exchanges with client...
        validate_cert = conn.recv(RECV_BYTES).decode()
        ca_s_pub_key, ca_s_priv_key, cert = ca_s_split(returned_des_contents)
        #print(cert, type(cert)); print(ca_s_pub_key, type(ca_s_pub_key)); print(ca_s_priv_key, type(ca_s_priv_key))
        
        # PRINTOUT 2
        print(PO[1][1])
        print(returned_des_key)
        print([ca_s_pub_key, ca_s_priv_key])
        print(cert, '\n\n')
        
        # Exit out of first-half of server, continue to serverProgram2 for rest of lab (client-server exchange).
        print("To continue the lab, open new terminal and type in the following:\n")
        print(f"\tpython3 main.py {CLIENT}")
        break
    
    s_socket.close()
    serverProgram2()
    
# for any communication between server and client
def serverProgram2():
    time.sleep(1)
    s_socket = socket(AF_INET, SOCK_STREAM)
    s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s_socket.bind((HOST, PORT))
    s_socket.listen(BACKLOG)
    
    while True:
        conn, addr = s_socket.accept()
        if conn : conn.send(str(INTERMEDIATE_PASS).encode())
        if (conn.recv(RECV_BYTES).decode() != JUNK): continue   # don't go anywhere until valid connection is made
    
        # RECV third exchange: C -> S
        recv_c_s_1 = conn.recv(RECV_BYTES).decode()
        returned_s_id, returned_c_s_1_ts = c_s_1_split(recv_c_s_1)
        
        # PRINTOUT 3
        print(PO[2][0])
        print(returned_s_id, returned_c_s_1_ts, '\n\n')
    
        # SEND fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        s_c_1_ts = str(ts())
        s_pub_key = read_key(S_PUB_KEY)
        s_c_1_concat = concat(s_pub_key, str(cert), s_c_1_ts)
        conn.send(str(s_c_1_concat).encode())
        
        # PRINTOUT 4
        print(PO[2][1])
        print(s_pub_key, cert, s_c_1_ts, '\n\n')
        
        # verify the contents of verificate
        conn.send(str(validate_cert).encode())
        conn.recv(RECV_BYTES)
        conn.send(str(ca_s_pub_key).encode())
        conn.recv(RECV_BYTES)
        conn.send(str(cert).encode())
        
        # RECV fifth exchange: C -> S
        s5_rsa_priv_key = begin_rsa(2)
        s5_rsa_pub_key = read_key(RSA_PUB_KEY_2, True)
        conn.send(str(s5_rsa_pub_key).encode())
        s5_recv = eval(conn.recv(RECV_BYTES).decode())
        conn.send(JUNK.encode())
        decrypted_rsa_s5 = rsacrypt(s5_rsa_priv_key[1], s5_rsa_priv_key[0], s5_recv)
        returned_rsa_s5 = digitize_text(DEC, decrypted_rsa_s5)
        assert returned_rsa_s5 == conn.recv(RECV_BYTES).decode(), "RSA Error: RSA decryption failed to correctly return valid string"
        returned_ktmp2 = returned_rsa_s5[:KEY_LEN]
        
        # PRINTOUT 5
        print(PO[3][1])
        print(s5_recv)
        print(returned_ktmp2, '\n\n')
        
        # SEND sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]  
        s6_ts = str(ts())
        new_sess_key = read_key(SESS_KEY)
        s6_concat = concat(new_sess_key, LT_SESS, ID_C, s6_ts)
        s6_send = descrypt(ENC, returned_ktmp2, s6_concat)
        conn.send(s6_send)
        
        # PRINTOUT 6
        print(PO[4][0])
        print(s6_send)
        print(new_sess_key, '\n\n')
        
        # RECV seventh exchange: C -> S
        s7_recv = conn.recv(RECV_BYTES)
        returned_s7_data = descrypt(DEC, new_sess_key, s7_recv).decode()
        returned_req, returned_s7_ts = c_s_3_split(returned_s7_data)
        
        # PRINTOUT 7
        print(PO[5][0])
        print(s7_recv)
        print('\nMessage:\t', returned_req, '\n\n')
        
        # SEND eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        s8_ts = str(ts())
        s8_concat = concat(DATA, s8_ts)
        s8_send = descrypt(ENC, new_sess_key, s8_concat)
        conn.send(s8_send)
        
        # PRINTOUT 8
        print(PO[5][1])
        print(s8_send)
        print('\nFinal message: \t', DATA, '\n\n')
        
        # EXTRA: https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
        break
        
    # Exiting out of everything.
    print("\nTerminating lab...\n\n")
    s_socket.close()
    sys.exit()
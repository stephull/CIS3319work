'''
    client.py       -- Main program for client (socket programming)
'''

from configurations import *
from gears import *

def client_side():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((LOCALHOST, PORT))

    print(f'Welcome. You are the client. Remember to type {EXIT_KEY} to exit...')
    
    # send input to server 
    msg = input(INPUT_STR)  ### S(1/10)

    # exit program by typing "-1" or pressing the 'Esc' key:
    while msg.lower().strip() != str(EXIT_KEY):

        # read from the file and encrypt message
        ciphertext = encrypt_msg(key, msg) ### S(2/10)
        format_msg(key, msg, ciphertext, ENC)
        
        # send the input, should send ciphertext
        client_socket.send(str(ciphertext).encode()) ### S(3/10)

        # ...

        data = client_socket.recv(RECV_BYTES).decode()    ### S(9/10)

        # decrypt + message 
        new_plaintext = decrypt_msg(key, data)  ### S(10/10)
        print(f'\nFROM: {SERVER}')
        format_msg(key, data, new_plaintext, DEC)

        # send input to server
        msg = input(INPUT_STR)

    client_socket.close()
    sys.exit()

if __name__ == '__main__':
    client_side()
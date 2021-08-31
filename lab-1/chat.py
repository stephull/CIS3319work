from socket import *

LOCALHOST = "127.0.0.1"
PORT = 8088
MAX_PORT = 49151
MIN_PORT = 1024
KEYFILE = "lab-1/key.txt"

def check_port(n):
    # we can only use ports between 1024 - 49151
    return n if (n <= MAX_PORT and n >= MIN_PORT) else -1

def generate_keyfile():
    f = open(KEYFILE, 'w')
    f.write('::: WRITING DES KEY TO FILE :::')
    f.close()

def main():
    # check if port is valid
    if (check_port(PORT) < 0):
        raise ValueError('\n\n :: PORT invalid, change to value between {} and {} :: \n'.format(MIN_PORT, MAX_PORT))
    print('PORT {} valid'.format(PORT))

    # generate key file 
    generate_keyfile()

    # create new server
    with socket(AF_INET, SOCK_STREAM) as s:
        pass
        '''
        s.bind((LOCALHOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Accepted new connection from {}'.format(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
        '''

    # create new client
    with socket(AF_INET, SOCK_STREAM) as s:
        pass
        '''
        s.connect((LOCALHOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)
        '''

if __name__ == "__main__":
    main()
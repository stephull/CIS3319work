from configurations import *
from socket import *

# create new client
def start_client():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((LOCALHOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)
    print('Received', repr(data))
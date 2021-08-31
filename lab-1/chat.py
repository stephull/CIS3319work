from socket import *
import os

LOCALHOST = "127.0.0.1"
PORT = 8765
MAX_PORT = 49151
MIN_PORT = 1024

def check_port(n):
    # we can only use ports between 1024 - 49151
    return n if (n <= MAX_PORT and n >= MIN_PORT) else -1

def main():
    pass

if __name__ == "__main__":
    main()
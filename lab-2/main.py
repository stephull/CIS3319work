# main.py
# Includes main executable method

from client import *
from server import *

def main():
    # check if the number of arguments is correct
    assert len(sys.argv) == ARGS_LENGTH
    command = sys.argv[1]

    # use assert statements to check PORT validity AND correct command argument
    assert PORT < PORT_MAX and PORT >= PORT_MIN
    assert command == str(SERVER) or command == str(CLIENT)

    # redirect to either server or client depending on which one user chooses:
    server_program() if command == SERVER else client_program()

if __name__ == "__main__":
    main()
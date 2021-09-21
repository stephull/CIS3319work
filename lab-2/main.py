# main.py
# Includes main executable method

from network import *

def main():
    # check if the number of arguments is correct
    assert len(sys.argv) == ARGS_LEN
    command = sys.argv[1]

    # use assert statements to check PORT validity AND correct command argument
    assert PORT < PORT_MAX and PORT >= PORT_MIN
    print(f'Using #{PORT} to connect...')

    # start program :-)
    assert command == SERVER or CLIENT
    server_program() if command == SERVER else client_program()

if __name__ == "__main__":
    main()
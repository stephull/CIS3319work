'''
    main.py     -- Main program for project
    ALWAYS start executable with 'python3 main.py <user>'
'''

from configurations import *
from gears import *
from server import *
from client import *

# first function, make sure all ports are within respective range
def check_port(n):
    return n if n <= MAX_PORT and n >= MIN_PORT else -1

# in our program, we ask for the client or server at the end
def check_args():
    if not len(sys.argv) == ARGS_LENGTH:
        raise AssertionError(f'\n\n :: Need {ARGS_LENGTH} arguments: {ARGS_HELP[0]} {ARGS_HELP[1]} :: \n')
    print('\nWelcome! The program is ready to start!\n')

# main method
def main():

    # check if arguments are correct
    check_args()

    # check if port is valid
    if (check_port(PORT) < 0):
        raise ValueError(f'\n\n :: PORT invalid, change to value between {MIN_PORT} and {MAX_PORT} :: \n')
    print(f'Using PORT #{PORT}...')

    # connect client and server into main program
    # IF argument asks for 'client' or 'server', give them the right interface
    # AND if client joins, generate key (assure that both client and server are present)
    if COMM != str(SERVER) and COMM != str(CLIENT):
        raise AssertionError(f'\n\n :: Must be {SERVER} or {CLIENT} for second argument, try again! :: \n')
    server_side() if (COMM == SERVER) else client_side()

# start program
if __name__ == "__main__":
    main()
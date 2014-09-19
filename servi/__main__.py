import sys
from command import process_and_run_command_line
from servi_exceptions import *


def main():
    try:
        process_and_run_command_line()
    except (ServiError, ForceError):
        return False


    sys.exit(0)

if __name__ == "__main__":
    main()
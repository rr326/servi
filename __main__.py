import os
from glob import glob
import argparse
from importlib import import_module
from servi_exceptions import *
import sys
import config as c
from command import process_and_run_command_line

def main():
    process_and_run_command_line()

    sys.exit(0)

if __name__ == "__main__":
    main()
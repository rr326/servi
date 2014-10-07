import sys
from servi.command import process_and_run_command_line
from servi.exceptions import ServiError, ForceError
from servi.config import LOG_LEVEL as DEFAULT_LOG_LEVEL
import logging


def setup_logging():
    # Set a default logger
    logging.basicConfig(level=DEFAULT_LOG_LEVEL, format='%(message)s')


def main():
    setup_logging()
    try:
        process_and_run_command_line()
    except (ServiError, ForceError) as e:
        sys.stderr.write(str(e))
        return False

    sys.exit(0)

if __name__ == "__main__":
    main()
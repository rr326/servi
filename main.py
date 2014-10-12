import sys
from servi.command import process_and_run_command_line
from servi.exceptions import ServiError, ForceError, MasterNotFound
from servi.config import DEFAULT_LOG_LEVEL as DEFAULT_LOG_LEVEL
import logging


def setup_logging():
    class MyFormatter(logging.Formatter):
        # http://stackoverflow.com/a/8349076/1400991
        def __init__(self, fmt="%(levelno)s: %(msg)s"):
            logging.Formatter.__init__(self, fmt)

        def format(self, record):
            if record.levelno >= logging.WARNING:
                fmt = '%(levelname)s: %(msg)s'
            else:
                fmt = '%(msg)s'

            self._fmt = fmt
            self._style = logging.PercentStyle(self._fmt)
            result = logging.Formatter.format(self, record)
            return result

    # Set a default logger
    fmt = MyFormatter()
    hdlr = logging.StreamHandler(sys.stdout)

    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)
    logging.root.setLevel(DEFAULT_LOG_LEVEL)


def main():
    setup_logging()
    try:
        retval = process_and_run_command_line()
    except (ServiError, ForceError, MasterNotFound) as e:
        logging.error(str(e))
        retval = False

    sys.exit(1 if not retval else 0)  # Linux error codes are reversed!

if __name__ == "__main__":
    main()
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
            if (record.levelno == logging.WARNING
                    or record.levelno > logging.ERROR):
                fmt = '%(levelname)s: %(msg)s'
            else:
                # Errors have my own ERROR text
                # Info/debug don't need a levelname
                fmt = '%(msg)s'

            self._fmt = fmt
            self._style = logging.PercentStyle(self._fmt)
            result = logging.Formatter.format(self, record)
            return result

    # http://stackoverflow.com/a/24956305/1400991

    class LevelFilter(logging.Filter):
        LT = 'LT'
        GTE = 'GTE'

        def __init__(self, level, comp):
            super().__init__()
            self.level = level
            self.comp = comp
            assert comp in [LevelFilter.LT, LevelFilter.GTE]

        def filter(self, record):
            if self.comp == LevelFilter.LT:
                return record.levelno < self.level
            else:
                return record.levelno >= self.level

    # Set a default logger
    fmt = MyFormatter()

    stdout_hdlr = logging.StreamHandler(sys.stdout)
    stdout_hdlr.setFormatter(fmt)
    lower_than_error = LevelFilter(logging.ERROR, LevelFilter.LT)
    stdout_hdlr.addFilter(lower_than_error)
    logging.root.addHandler(stdout_hdlr)

    stderr_hdlr = logging.StreamHandler(sys.stderr)
    stderr_hdlr.setFormatter(fmt)
    gte_than_error = LevelFilter(logging.ERROR, LevelFilter.GTE)
    stderr_hdlr.addFilter(gte_than_error)
    logging.root.addHandler(stderr_hdlr)

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
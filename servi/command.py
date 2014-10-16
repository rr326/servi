from glob import glob
import argparse
import sys
import io
from importlib import import_module
import os
from servi.exceptions import ForceError, ServiError
import servi.config as c
from servi.config import set_master_dir, load_user_config
from logging import debug, info, warning as warn, error
import logging
from contextlib import contextmanager


class Command(object):
    def __init__(self):
        self.special = {
            "skip_init": False,
            "parse_known_args": False
        }

    def register_command_line(self, sub_parser):
        pass

    def run(self, args, extra_args):
        pass


def find_plugins():
    plugins = []
    for f in glob(os.path.dirname(__file__) + '/commands/*.py'):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            plugins.append(os.path.basename(f)[:-3])

    return plugins


# noinspection PyUnresolvedReferences
def load_plugins(main_parser):
    """
    Loads plugins from ./commands directory.
    Each plugin must implement Command.Command class.
    """
    import servi.commands  # required for import_module()
    plugins = find_plugins()
    command_dict = {}
    for plugin in plugins:
        mod = import_module('servi.commands.'+plugin, package='servi.commands')
        p = command_dict[plugin] = mod.command
        p.register_command_line(main_parser)

    return command_dict


# Override handling of argparse errors to print whole help
# http://stackoverflow.com/a/16942165/1400991
class ArgumentParserMod(argparse.ArgumentParser):
    def error(self, message):
        # sys.stderr.write('***********\n%s: error: %s\n\n' % (self.prog, message))
        # self.print_help(sys.stderr)
        # self.exit(2)
        stream = io.StringIO()
        self.print_help(stream)
        errmsg = '%s: error: %s\n\n' % (self.prog, message) \
                 + str(stream.getvalue())
        raise ServiError(errmsg)


def setup_parsers():
    servi_parser = ArgumentParserMod(
        description='Servi Main Commands',
        usage='servi [global options] COMMAND [command options]')

    # Only for testing
    servi_parser.add_argument('--template_dir', type=str,
                              help=argparse.SUPPRESS)

    servi_parser.add_argument(
        '-v', '--verbose', type=int, choices=range(0, 5),
        help='4: debug, 3: info, 2: warn, 1: error, 0: silent'
             '(Note: -v0 is risky since errors are not displayed)',
        default=log_level_to_arg(c.DEFAULT_LOG_LEVEL))

    sub_parsers = servi_parser.add_subparsers(
        title='Commands', metavar='', dest='command', prog='servi')

    return servi_parser, sub_parsers


def parse_args(commands, servi_parser, command_line):
    """
    Returns parse arguments

    This is a bit complicated because we need to do a
    preparse to figure out which command (eg: 'lans'):

        * If commands[command].special["parse_known_args"]:
            * return parsed known_args
        * else
            * return parsed all_args

    """
    cmdline_ar = command_line.split() if command_line else None

    args = servi_parser.parse_known_args(cmdline_ar)

    if not args[0].command in commands:
        return args
    else:
        special = getattr(commands[args[0].command], "special", {})
        if special.get("parse_known_args", False):
            return args
        else:
            args = servi_parser.parse_args(cmdline_ar)
            return args, []


@contextmanager
def use_log_level(log_level):
    logger = logging.getLogger()
    orig_level = logger.getEffectiveLevel()
    logger.setLevel(log_level)
    yield
    logger.setLevel(orig_level)


def arg_to_log_level(arglevel):
    return (5 - arglevel)*10


def log_level_to_arg(level):
    return 5 - int(level/10)


def process_and_run_command_line(command_line=None):
        servi_parser, sub_parsers = setup_parsers()

        commands = load_plugins(sub_parsers)

        args, extra_args = parse_args(commands, servi_parser, command_line)

        log_level = arg_to_log_level(args.verbose)
        with use_log_level(log_level):
            if args.template_dir:
                c.TMPL_DIR_SITE = args.template_dir
                warn('*** WARNING: Just set TMPL_DIR_SITE to |{0}|'.format(
                    c.TMPL_DIR_SITE))

            if not args.command:
                error('\n***** Error ******\nNo command on command line.\n')
                servi_parser.print_help()
                raise ServiError('No command line')

            if args.command not in commands:
                raise ServiError('Unknown command: {0}'.format(args.command))

            special = getattr(commands[args.command], "special", {})

            if not special.get("skip_init", False):
                master_dir = c.find_master_dir(os.getcwd())
                set_master_dir(master_dir)
                load_user_config()

            try:
                info('Servi - Running: {0}\n'.format(args.command))
                if c.MASTER_DIR:
                    debug('Master Directory: {0}'
                        .format(os.path.abspath(c.MASTER_DIR)))
                debug('Template Directory: {0}'
                    .format(os.path.abspath(c.TMPL_DIR_SITE)))

                retval = args.command_func(args, extra_args)
            except (ForceError, ServiError) as e:
                raise


        return retval
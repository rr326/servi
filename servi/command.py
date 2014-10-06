from glob import glob
import argparse
from importlib import import_module
import os
from servi.exceptions import ForceError, ServiError
import servi.config as c
from servi.config import set_master_dir, load_user_config
from servi.utils import qprint
import servi.globals as g


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


def setup_parsers():
    servi_parser = argparse.ArgumentParser(
        description='Servi Main Commands')

    # Only for testing
    servi_parser.add_argument('--template_dir', type=str,
                              help=argparse.SUPPRESS)
    servi_parser.add_argument('-q', '--quiet', action='store_true')

    sub_parsers = servi_parser.add_subparsers(
        title='Commands', metavar='', dest='command')

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


def process_and_run_command_line(command_line=None):
        servi_parser, sub_parsers = setup_parsers()

        commands = load_plugins(sub_parsers)

        args, extra_args = parse_args(commands, servi_parser, command_line)

        if args.quiet:
            g.quiet = True

        if args.template_dir:
            c.TMPL_DIR_SITE = args.template_dir
            print('*** WARNING: Just set TMPL_DIR_SITE to |{0}|'.format(
                c.TMPL_DIR_SITE))

        if not args.command:
            print('\n***** Error ******\nNo command on command line.\n')
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
            qprint('Servi - Running: {0}\n'.format(args.command))
            retval = args.command_func(args, extra_args)
        except (ForceError, ServiError) as e:
            print(e)
            raise


        return retval
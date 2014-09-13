import os
from glob import glob
import argparse
from importlib import import_module
from servi_exceptions import *
import sys
import config as c


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
    import commands  # required for import_module()
    plugins = find_plugins()
    command_dict = {}
    for plugin in plugins:
        mod = import_module('commands.'+plugin, package='commands')
        p = command_dict[plugin] = mod.command
        p.register_command_line(main_parser)


def main():
    global servi_parser
    servi_parser = argparse.ArgumentParser(description='Servi Main Commands')

    # Only for testing
    servi_parser.add_argument('--template_dir', type=str, help=argparse.SUPPRESS)

    sub_parsers = servi_parser.add_subparsers(
        title='Commands', metavar='', dest='command')

    load_plugins(sub_parsers)

    args = servi_parser.parse_args()

    if args.template_dir:
        c.TEMPLATE_DIR = args.template_dir
        print('*** WARNING: Just set TEMPLATE_DIR to |{0}|'.format(c.TEMPLATE_DIR))

    if args.command:
        try:
            print('Servi - Running: {0}\n'.format(args.command))
            args.command_func(args)
        except (ForceError, ServiError) as e:
            print(e)
            sys.exit("Servi Error. Aborting.")
    else:
        print('\n***** Error ******\nNo command on command line.\n')
        servi_parser.print_help()
        sys.exit("Error - No command line. Aborting")

    sys.exit(0)

if __name__ == "__main__":
    main()
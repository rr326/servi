from glob import glob
import os
import argparse
from servi.servi_exceptions import *
import servi.config as c
from importlib import import_module
from servi.utils import find_master_dir
from servi.getconfig import getconfig

class Command(object):
    def __init__(self):
        pass

    def register_command_line(self, sub_parser):
        pass

    def run(self, args):
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


def setup_parsers():
    servi_parser = argparse.ArgumentParser(
        description='Servi Main Commands')

    # Only for testing
    servi_parser.add_argument('--template_dir', type=str,
                              help=argparse.SUPPRESS)

    sub_parsers = servi_parser.add_subparsers(
        title='Commands', metavar='', dest='command')

    return servi_parser, sub_parsers


def set_master_dir(set_dir_to=None):
    """
    sets c.MASTER_DIR
        by finding the first ancestor(default)
        to set_dir_to (if supplied - only for servi init)
    """
    if not dir:
        c.MASTER_DIR = find_master_dir()
    else:
        c.MASTER_DIR = set_dir_to

    c.MSTR_TMPL_DIR = None if not c.MASTER_DIR else \
        os.path.normpath(os.path.join(c.MASTER_DIR, 'servi/servi_templates'))


def load_user_config():
    user_config = getconfig(
        c.SERVI_CONFIG_YML, c.TEMPLATE, c.MASTER, c.MSTR_TMPL_DIR,
        c.MASTER_DIR)

    for key, value in user_config.items():
        setattr(c,key, value)


def process_and_run_command_line(command_line=None):
        servi_parser, sub_parsers = setup_parsers()

        load_plugins(sub_parsers)

        if command_line:
            args = servi_parser.parse_args(command_line.split())
        else:
            args = servi_parser.parse_args()

        if args.template_dir:
            c.MSTR_TMPL_DIR = args.template_dir
            print('*** WARNING: Just set MSTR_TMPL_DIR to |{0}|'.format(
                c.MSTR_TMPL_DIR))

        if args.command:
            try:
                if args.command != 'init':
                    # An uninitialized space is special
                    set_master_dir()
                    load_user_config()
                print('Servi - Running: {0}\n'.format(args.command))
                retval = args.command_func(args)
            except (ForceError, ServiError) as e:
                print(e)
                raise
        else:
            print('\n***** Error ******\nNo command on command line.\n')
            servi_parser.print_help()
            raise ServiError('No command line')

        return retval
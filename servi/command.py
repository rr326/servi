from glob import glob
import argparse
from importlib import import_module

from servi.servi_exceptions import *
import servi.config as c

from servi.config import set_master_dir, load_user_config


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


def process_and_run_command_line(command_line=None):
        servi_parser, sub_parsers = setup_parsers()

        load_plugins(sub_parsers)

        if command_line:
            args = servi_parser.parse_args(command_line.split())
        else:
            args = servi_parser.parse_args()

        if args.template_dir:
            c.TMPL_DIR_SITE = args.template_dir
            print('*** WARNING: Just set TMPL_DIR_SITE to |{0}|'.format(
                c.TMPL_DIR_SITE))

        if not args.command:
            print('\n***** Error ******\nNo command on command line.\n')
            servi_parser.print_help()
            raise ServiError('No command line')

        if args.command not in ['init', 'zz']:
            master_dir = c.find_master_dir(os.getcwd())
            set_master_dir(master_dir)
            load_user_config()

        try:
            print('Servi - Running: {0}\n'.format(args.command))
            retval = args.command_func(args)
        except (ForceError, ServiError) as e:
            print(e)
            raise


        return retval
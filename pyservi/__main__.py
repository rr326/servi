import os
from glob import glob
import argparse
from importlib import import_module
from servi_exceptions import ForceError


def find_plugins():
    plugins = []
    for f in glob(os.path.dirname(__file__) + '/commands/*.py'):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            plugins.append(os.path.basename(f)[:-3])

    return plugins


def load_plugins(main_parser):
    """
    Loads plugins from ./commands directory.
    Each plugin must implement Command.Command class.
    """
    import commands  # required for import_module()
    plugins = find_plugins()
    print('Plugins found: {0}'.format(plugins))
    command_dict = {}
    for plugin in plugins:
        mod = import_module('commands.'+plugin, package='commands')
        p = command_dict[plugin] = mod.command
        p.register_command_line(main_parser)


def main():
    print('servi.__main__.py main()')
    main_parser = argparse.ArgumentParser(description='Servi Main Commands')
    sub_parsers = main_parser.add_subparsers(title='Commands', metavar='')

    load_plugins(sub_parsers)

    args = main_parser.parse_args()
    try:
        args.command_func(args)
    except ForceError as e:
        print(e)

if __name__ == "__main__":
    main()
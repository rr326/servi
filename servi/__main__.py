import os
from glob import glob
import argparse
from importlib import import_module
from servi_exceptions import ForceError



# import argparse
# import os
# from glob import glob
#
# def load_plugins():
#     all_list=[]
#     for f in glob(os.path.dirname(__file__)+'/commands/*.py'):
#         if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
#             all_list.append(os.path.basename(f)[:-3])
#
#     return all_list
#
#
# def parse_args():
#     parser = argparse.ArgumentParser(description='Servi Main Commands')
#
#     subparsers = parser.add_subparsers(title='Commands', metavar='')
#
#     parser_init = subparsers.add_parser('init', help='Initialize project')
#     parser_init.add_argument('-f', '--force', action='store_true')
#     parser_init.set_defaults(command_func=servi_init.run)
#
#     subparsers.add_parser('update', help='Update project')
#
#     args = parser.parse_args()
#     print(args)
#     args.command_func(args)
#     pass
#
#
# def main():
#     #parse_args()
#     commands = load_plugins()
#     print('commands: {0}'.format(commands))


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
    import commands
    plugins = find_plugins()
    print('Plugins found: {0}'.format(plugins))
    commands={}
    for plugin in plugins:
        mod = import_module('commands.'+plugin, package='commands')
        p = commands[plugin] = mod.command
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
# import argparse
# import os
# from glob import glob
#
# def import_commands():
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
#     commands = import_commands()
#     print('commands: {0}'.format(commands))
def main():
    print('servi.__main__.py main()')

if __name__ == "__main__":
    main()
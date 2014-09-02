import argparse
import servi_init


def parse_args():
    parser = argparse.ArgumentParser(description='Servi Main Commands')

    subparsers = parser.add_subparsers(title='Commands', metavar='')

    parser_init = subparsers.add_parser('init', help='Initialize project')
    parser_init.add_argument('-f', '--force', action='store_true')
    parser_init.set_defaults(command_func=servi_init.run)

    subparsers.add_parser('update', help='Update project')

    args = parser.parse_args()
    print(args)
    args.command_func(args)


def main():
    parse_args()

if __name__ == "__main__":
    main()
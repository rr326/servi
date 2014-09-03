from config import *
from Command import Command
from commands._commands_utils import *
from servi_exceptions import ForceError


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-f', '--force', action='store_true')
        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        print('update.run() called with args: {0}'.format(args))


command = UpdateCommand()

## TODO - How to deal with files that were deleted in MASTER_DIR
## (eg: THIS_SITE.conf)
import os
import shutil
from logging import info
from datetime import datetime

from servi.command import Command

from servi.utils import pathfor
import servi.config as c
from servi.exceptions import ServiError, ForceError
from servi.template_mgr import TemplateManager as TMgr


class CopyCommand(Command):
    def __init__(self):
        super().__init__()
        self.parser = None
        self.arglist = None

    # noinspection PyProtectedMember
    def register_command_line(self, sub_parsers):

        #
        # Note - this is as-defined by ansible:
        # http://docs.ansible.com/developing_inventory.html
        #
        parser = sub_parsers.add_parser(
            'copy', help='Copy template file to master',
            description='Copy template file to master, overwriting '
                        'master if it exists. Use this if a file in your '
                        'template and master have both changed but you '
                        'want to overwrite the master anyway. '
                        'Do a "servi diff" first to see changes. '
                        'Requires the -f/--force flag.')

        parser.add_argument(
            'template_file_name', type=str,
            help='relative path (base=Servifile.yml directory)')

        parser.add_argument('-f', '--force', action='store_true')

        parser.set_defaults(command_func=self.run)

        self.parser = parser
        self.arglist = [arg.dest for arg in parser._optionals._actions
                        if arg.dest != 'help']

    def run(self, args, extra_args):
        source = pathfor(args.template_file_name, c.TEMPLATE)
        if not os.path.exists(source):
            raise ServiError('File does not exist\n'
                             'Given path: {0}\n'
                             'Template path: {1}\n'
                             .format(args.template_file_name, source))

        dest = pathfor(args.template_file_name, c.MASTER)
        if os.path.exists(dest):
            if not args.force:
                raise ForceError('Dest file exists: {0}'
                                 .format(os.path.abspath(dest)))
            else:
                TMgr.rename_master_file(args.template_file_name,
                                        datetime.now())

        shutil.copy2(source, dest)
        info('Copied {0} to {1}'.format(source, dest))

        return True


command = CopyCommand()





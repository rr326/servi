import subprocess
import os
from logging import debug, info, warning as warn, error
import tempfile

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor, timeit
from servi.exceptions import ServiError
from servi.commands.lans import get_servi_inventory_path
from pprint import pformat


class RansCommand(Command):
    def __init__(self):
        super().__init__()
        self.special = {"parse_known_args": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'rans', help="Remote ANSible - "
                         "Run ansbile on your remote system.",
            description="Remote ANSible - "
                        "Run ansbile on your remote system."
                        "This is a convenience function that sets "
                        "up the ansible command with the proper "
                        "vagrant_inventory "
                        "file, and ssh user and password, saving you a lot "
                        "of typing. Any arguments not listed below will be "
                        "passed directly 'ansible-playbook'."
        )

        parser.add_argument(
            '-p', '--project_only', action='store_true', help=
            'Only run the "projectSpecific" role.')

        parser.add_argument(
            'host_alias',
            help='alias of host to run ansible on. '
                 'This is the key part of the HOSTS field in'
                 'Servifile_globals.yml or Servifile.yml ')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        hostdict = c.HOSTS

        if args.host_alias not in hostdict:
            raise ServiError('Given host alias ({0}) not found in '
                             'Servifile_globals.yml or Servifile.yml '
                             'HOSTS: \n{1}'
                             .format(args.host_alias, pformat(c.HOSTS)))

        alias = args.host_alias
        proj_only = ['-t', 'projectSpecific'] if args.project_only else []
        is_vagrant = \
            c.HOSTS \
            .get(args.host_alias, {}) \
            .get("vars", {}) \
            .get("IS_VAGRANT", False)

        cmd_line = ['ansible-playbook', 'playbook.yml',
                    '--inventory-file', get_servi_inventory_path(),
                    '--limit', alias,
                    '--user', c.MAIN_USERNAME,
                    '--private-key', c.MAIN_RSA_KEY_FILE,
                    '-e', "IS_VAGRANT={0}".format(is_vagrant),
                    ] + proj_only \
                      + extra_args

        info('Running REMOTE ansible with:\n\tcommand line: {0}\n\tcwd:{1}'
             .format(' '.join(cmd_line),
                     os.path.join(c.MASTER_DIR, 'ansible_config')))

        with timeit():
            retval = subprocess.call(
                cmd_line, cwd=os.path.join(c.MASTER_DIR, 'ansible_config'))

        return not retval


command = RansCommand()

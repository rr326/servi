import subprocess
import os
from logging import debug, info, warning as warn, error

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor, timeit
from servi.exceptions import ServiError
import sys


def get_servi_inventory_path():
    try:
        servi_inventory = \
            subprocess.check_output('which servi_inventory', shell=True,
                                    universal_newlines=True)
    except subprocess.CalledProcessError:
        raise ServiError("Couldn't find servi_inventory script on path.\n"
                         "Try 'which servi_inventory'.\n"
                         "Current path: {0}".format(sys.path))
    servi_inventory = servi_inventory.strip()

    return servi_inventory


class LansCommand(Command):
    def __init__(self):
        super().__init__()
        self.special = {"parse_known_args": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'lans', help="Local ANSible - "
                         "Run ansbile on your local (vagrant) setup.",
            description="Local ANSible - "
                        "Run ansbile on your local (vagrant) setup."
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

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        proj_only = ['-t', 'projectSpecific'] if args.project_only else []

        cmd_line = ['ansible-playbook', 'playbook.yml',
                    '--inventory-file', get_servi_inventory_path(),
                    '--limit', 'vagrant',
                    '--user', c.MAIN_USERNAME,
                    '--private-key', c.MAIN_RSA_KEY_FILE,
                    '-e', 'IS_VAGRANT=True',
                    ] + proj_only \
                      + extra_args

        info('Running local ansible with:\n\tcommand line: {0}\n\tcwd:{1}'
             .format(' '.join(cmd_line),
                     os.path.join(c.MASTER_DIR, 'ansible_config')))

        with timeit():
            retval = subprocess.call(
                cmd_line, cwd=os.path.join(c.MASTER_DIR, 'ansible_config'))

        return not retval


command = LansCommand()

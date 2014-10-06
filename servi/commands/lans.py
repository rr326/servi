import subprocess
import os

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor


class LansCommand(Command):
    def __init__(self):
        self.special = {"parse_known_args": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'lans', help="Local ANSible - "
                         "Run ansbile on your local (vagrant) setup.",
            description="Local ANSible - "
                        "Run ansbile on your local (vagrant) setup."
                        "This is a convenience function that sets "
                        "up the ansible command with the proper inventory "
                        "file, and ssh user and password, saving you a lot "
                        "of typing. Any arguments not listed below will be "
                        "passed directly 'ansible-playbook'."
        )

        parser.add_argument(
            '-p', '--project_only', action='store_true', help=
            'Only run the "projectSpecific" role.')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):

        print('*'*100)
        print('Lans running. \n\tArgs: {0}\n\textra_args: {1}'.format(args, extra_args))
        return True


command = LansCommand()

"""
TODO
* Setup CommandClass to have special options
    * do init/skip_init
    * parse all args / parse known args

* Then for lans, do parse known args
"""
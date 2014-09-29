import subprocess
import os

from servi.command import Command, process_and_run_command_line as servi_run
import servi.config as c
from servi.utils import pathfor
from tempfile import TemporaryDirectory
from servi.template_mgr import TemplateManager
import re
from servi.commands.buildbox import get_boxname
from servi.exceptions import ServiError


class UseboxCommand(Command):
    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'usebox', help="Use a vagrant base box that you already "
                           "created with 'servi buildbox'.",
            description=
            "Use a vagrant base box that you already built with "
            "'servi buildbox'.\n"
            "See 'servi buildbox --help' for more information'"
        )

        parser.set_defaults(command_func=self.run)

    def run(self, args):
        box_name, box_path = get_boxname()

        env = os.environ.copy()
        env['servi_box']= box_path

        if not os.path.exists(box_path):
            raise ServiError('A current servi_box does not exist.\n'
                             'Be sure to run "servi buildbox" first.\n'
                             'Looking for: {0}'.format(box_path))

        # Other tests here
        # 1) ServiFile exists, Vagrant already up

        os.chdir(c.MASTER_DIR)
        subprocess.check_call(['vagrant', 'up'], env=env)

        return True


command = UseboxCommand()

# TODO - add command line parameters pass-through

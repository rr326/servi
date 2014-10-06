import subprocess
import os

from servi.command import Command, process_and_run_command_line as servi_run
import servi.config as c
from servi.utils import pathfor, timeit
from tempfile import TemporaryDirectory
from servi.template_mgr import TemplateManager
import re
from servi.commands.buildbox import get_boxname, get_all_boxes
from servi.exceptions import ServiError, ForceError
from servi.semantic import SemanticVersion
import argparse

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

        parser.add_argument('-f', '--force', action='store_true')

        # for testing
        parser.add_argument('--mock', action='store_true',
                            help=argparse.SUPPRESS)

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        all_boxes = get_all_boxes()
        if len(all_boxes) is 0:
            raise ServiError('No saved boxes found. Run "servi buildbox".')

        ver = all_boxes[0][1]
        tmgr = TemplateManager()
        if not args.force and ver < tmgr.m_template.template_version:
            raise ForceError('Existing saved servi_box has a version less '
                             'than existing template version.\n'
                             'Either run "servi buildbox" or run '
                             '"servi usebox --force."\n'
                             'Template version: {0}\n'
                             'servi_box: {1}'
                             .format(tmgr.m_template.template_version,
                             all_boxes[0][0]))

        env = os.environ.copy()
        env['servi_box']= os.path.join(c.BOX_DIR, all_boxes[0][0])

        os.chdir(c.MASTER_DIR)

        if not args.mock:
            with timeit():
                subprocess.check_call('vagrant up', env=env, shell=True)
        else:
            print('mocking vagrant up with base box: {0}'
                  .format(env['servi_box']))

        return True


command = UseboxCommand()


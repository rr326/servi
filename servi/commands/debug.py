import subprocess
import os
from logging import debug, info, warning as warn, error

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
from pprint import pformat
from copy import deepcopy

class DebugCommand(Command):
    # def __init__(self):
    #     # self.special = {"skip_init": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'debug', help="debug tools",
            description=
            "Process and display your rendered {0} and {1}"
                .format(c.SERVIFILE_GLOBAL_FULL, c.SERVIFILE)
        )



        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):

        global_config, user_config = c.load_user_config()
        combined = deepcopy(global_config)
        combined.update(user_config)

        info('\nGlobal config: \n{0}'.format(pformat(global_config, indent=4)))
        info('\nUser config: \n{0}\n'.format(pformat(user_config, indent=4)))
        info('\nCombined config: \n{0}\n'.format(pformat(combined, indent=4)))
        return True


command = DebugCommand()


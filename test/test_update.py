from test.fixtures import clean_master, mock_template_dir, servi_init, \
    process_succeeded, process_failed
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import pathfor
import config as c
from command import process_and_run_command_line as servi_run


import subprocess
import re

pytestmark = pytest.mark.wip


def test_update(clean_master, mock_template_dir, servi_init):
    # Modify a template file (that is clean in the master)
    file = 'ansible_config/roles/baseUbuntu/tasks/main.yml'
    print('test_update - TEMPLATE_DIR: ', c.TEMPLATE_DIR)
    with open(pathfor(file, c.TEMPLATE), 'a') as fp:
        fp.write('\n#NEW STUFF APPENDED HERE\n')

    # use the --template_dir so that you can pass a monkeypatched TEMPLATE_DIR
    # (such as from mock_template_dir) to the new process
    # update should succeed
    # assert servi_run('--template_dir {0} update'.format(c.TEMPLATE_DIR))



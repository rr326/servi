from test.fixtures import clean_master, mock_template_dir, servi_init, \
    process_succeeded, process_failed
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import pathfor
import config

import subprocess
import re

pytestmark = pytest.mark.wip


def test_update(clean_master, mock_template_dir, servi_init):
    # Modify a template file (that is clean in the master)
    file = 'ansible_config/roles/baseUbuntu/tasks/main.yml'
    print('test_update - TEMPLATE_DIR: ', config.TEMPLATE_DIR)
    with open(pathfor(file, config.TEMPLATE), 'a') as fp:
        fp.write('\n#NEW STUFF APPENDED HERE\n')

    # update should succeed
    assert process_succeeded(subprocess.call('python servi update',
                                             shell=True))

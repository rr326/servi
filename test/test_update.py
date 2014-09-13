from test.fixtures import clean_master, mock_template_dir, servi_init, \
    process_succeeded, process_failed
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import pathfor
import config as c

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
    assert process_succeeded(subprocess.call('python servi --template_dir {0} update'.format(c.TEMPLATE_DIR),
                                             shell=True))


# TODO - I probably have to add back the --template_dir command line parameter and then parameterize my servi_init fixture (or all them) with the template_dir.  Running it as a subprocess is what is killing me. I think.
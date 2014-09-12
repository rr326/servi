from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re

pytestmark = pytest.mark.wip


def test_update(clean_master, servi_init):
    # Modify a template file (that is clean in the master)
    file = 'ansible_config/playbook.yml'
    with open(file, 'a') as fp:
        fp.write('\n#NEW STUFF APPENDED HERE\n')

    # update should succeed
    assert process_succeeded(subprocess.call('python servi update',
                                             shell=True))

from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re


def test_dirty(clean_master, servi_init, dirty_master):
    # init should fail (since Master has been updated)
    assert subprocess.call('python servi init', shell=True)

    # update should also fail
    assert subprocess.call('python servi update', shell=True)

    # init -f should succeed (force)
    assert not subprocess.call('python servi init -f', shell=True)



from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re


def test_clean(clean_master, servi_init ):
    # init on a clean directory should work
    assert not subprocess.call('python servi init', shell=True)

    # Update on a clean directory should work too
    assert not subprocess.call('python servi update', shell=True)


from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re


def test_empty(clean_master, servi_init):
    m = mfest.Manifest(c.TEMPLATE)
    for file, sha1 in m.manifest["files"].items():
        if re.search(c.VERSION_FILE+'$', file):
            continue
        assert file_exists(pathfor(file, c.MASTER))


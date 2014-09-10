from test.fixtures import *
import pytest
from commands.utils.utils import *
import subprocess
import os
import commands.utils.manifest as man


def test_zz_save_manifest():
    os.remove(pathfor(MANIFEST_FILE, TEMPLATE))
    retval = subprocess.call('python servi zz --save_manifest', shell=True)
    assert not retval
    assert file_exists(pathfor(MANIFEST_FILE, TEMPLATE))
    # While we're at it, let's test that it's a good manifest, and that
    # manifest.load works
    new_man = man.Manifest(TEMPLATE)
    new_man.load()
    assert "files" in new_man.manifest

# test_zz_bump()
# Skipping - it actually bumps the Template version and I don't want to have
# to work around that.
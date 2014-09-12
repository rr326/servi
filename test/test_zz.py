from test.fixtures import *
import pytest
from commands.utils.utils import *
import subprocess
import os
import commands.utils.manifest as man
import tempfile


def test_zz_save_manifest():
    fp = tempfile.NamedTemporaryFile(delete=False)
    tmp_filename = fp.name
    fp.close()
    shutil.copy2(pathfor(c.VERSION_FILE, c.TEMPLATE), tmp_filename)

    try:
        os.remove(pathfor(c.MANIFEST_FILE, c.TEMPLATE))
        retval = subprocess.call('python servi zz --save_manifest', shell=True)
        assert not retval
        assert file_exists(pathfor(c.MANIFEST_FILE, c.TEMPLATE))
        # While we're at it, let's test that it's a good manifest, and that
        # manifest.load works
        new_man = man.Manifest(c.TEMPLATE, load=True)
        assert "files" in new_man.manifest
    except:
        # raise anything
        raise
    finally:
        # No matter what, revert VERSION_FILE
        shutil.copy2(tmp_filename, pathfor(c.VERSION_FILE, c.TEMPLATE))
        os.remove(tmp_filename)

# test_zz_bump()
# Skipping - it actually bumps the Template version and I don't want to have
# to work around that.
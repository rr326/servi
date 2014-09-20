from .fixtures import *
from commands.utils.utils import *
import os
import commands.utils.manifest as man
from command import process_and_run_command_line as servi_run


def test_zz_update_manifest(mock_template_dir):
    # Test changed manifest
    modify_file(pathfor('ansible_config/playbook.yml', c.TEMPLATE))
    assert servi_run('zz --update_manifest')

    # Now test skipping
    assert not servi_run('zz --update_manifest')

    # Test no manifest
    os.remove(pathfor(c.MANIFEST_FILE, c.TEMPLATE))
    assert servi_run('zz --update_manifest')
    assert file_exists(pathfor(c.MANIFEST_FILE, c.TEMPLATE))

    # While we're at it, let's test that it's a good manifest, and that
    # manifest.load works
    new_man = man.Manifest(c.TEMPLATE, load=True)
    assert "files" in new_man.manifest


# test_zz_bump()
# Skipping - it actually bumps the Template version and I don't want to have
# to work around that.
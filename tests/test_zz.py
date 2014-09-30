from tests.fixtures import *
from servi.utils import *
import servi.manifest as man
from servi.command import process_and_run_command_line as servi_run
from servi.utils import file_exists
from servi.semantic import SemanticVersion


def test_zz_update_manifest(mock_template_dir):
    pass
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

    with pytest.raises(Exception):
        servi_run('zz --update_manifest --bump minor')

    assert servi_run('zz --set_ver 1.0.0')
    assert servi_run('zz --bump patch')
    m = man.Manifest(c.TEMPLATE)
    assert m.template_version == SemanticVersion('1.0.1')


# test_zz_bump()
# Skipping - it actually bumps the Template version and I don't want to have
# to work around that.
from tests.fixtures import *
import servi.manifest as man
from servi.command import process_and_run_command_line as servi_run
from servi.utils import file_exists, reset_cwd
from servi.semantic import SemanticVersion
from servi.exceptions import ServiError
import subprocess
from filecmp import cmp
from servi.commands.utils import in_servi_code_dir


def test_cmd_utils(mock_template_dir, mock_in_servi_dir):
    # Test changed manifest
    modify_file(pathfor('ansible_config/playbook.yml', c.TEMPLATE))
    assert not servi_run('utils --ensure_latest_manifest')

    # Now test skipping
    assert servi_run('utils --ensure_latest_manifest')

    # Test no manifest
    os.remove(pathfor(c.MANIFEST_FILE, c.TEMPLATE))
    assert not servi_run('utils --ensure_latest_manifest')
    assert file_exists(pathfor(c.MANIFEST_FILE, c.TEMPLATE))

    # While we're at it, let's test that it's a good manifest, and that
    # manifest.load works
    new_man = man.Manifest(c.TEMPLATE, load=True)
    assert "files" in new_man.manifest

    # Only 1 at a time
    with pytest.raises(ServiError):
        servi_run('utils --ensure_latest_manifest --bump minor')

    assert servi_run('utils --set_ver 1.0.0')
    assert servi_run('utils --bump patch')
    m = man.Manifest(c.TEMPLATE)
    assert m.template_version == SemanticVersion('1.0.1')


def test_ensure_latest_globals_in_git(setup_empty, tmpdir):
    """
    Scenarios:
        * No ~/Servifile_globals.yml --> True
        * Not in git directory --> Raise
        * No local version --> copy & False
        * Different local version  --> copy & False
        * Same local version --> True
    """
    # Setup mocked servi directory
    servidir = tmpdir.mkdir('mockservi')
    projdir = tmpdir.mkdir('myproject')
    subprocess.call('git init '+str(servidir), shell=True)

    #
    # In Project Dir
    #
    projdir.chdir()
    assert servi_run('init --skip_servifile_globals .' )
    assert servi_run('utils --ensure_latest_globals_in_git ')

    assert servi_run('init -f .')
    with pytest.raises(ServiError):
        assert servi_run('utils --ensure_latest_globals_in_git')

    #
    # In Servi Dir
    #
    servidir.chdir()
    assert not servi_run('utils --ensure_latest_globals_in_git ')
    assert servidir.join(c.SERVIFILE_GLOBAL).check(exists=1)
    modify_file(c.SERVIFILE_GLOBAL_FULL)
    assert not servi_run('utils --ensure_latest_globals_in_git ')
    assert cmp(c.SERVIFILE_GLOBAL_FULL,
               str(servidir.join(c.SERVIFILE_GLOBAL)), shallow=False)

    assert servi_run('utils --ensure_latest_globals_in_git ')


def test_in_servi_code_dir(tmpdir):
    import py.path

    projdir = tmpdir.mkdir('myproject')
    thisdir = py.path.local(os.path.dirname(__file__))
    servidir = thisdir.join('..')
    with reset_cwd():
        servidir.chdir()
        assert in_servi_code_dir()
        subdir = servidir.join('tests')
        subdir.chdir()
        assert in_servi_code_dir()
        projdir.chdir()
        assert not in_servi_code_dir()


def test_link_githook(setup_init):
    with pytest.raises(ServiError):  # Not in git dir
        servi_run('utils --link_githook')

    subprocess.call('git init .', shell=True)
    assert servi_run('utils --link_githook')

    with pytest.raises(ServiError):  # Already exists
        servi_run('utils --link_githook')


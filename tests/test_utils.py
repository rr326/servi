from servi.config import find_master_dir
from tests.fixtures import *
from servi.exceptions import MasterNotFound
from servi.command import process_and_run_command_line as servi_run

@pytest.fixture()
def fake_master(tmpdir):
    """
    parent
        /master
            /servi
                \servi_templates
    """
    nonmaster = tmpdir.mkdir('nonmaster')
    master = tmpdir.mkdir('master')
    master.chdir()
    servi_run('init .')

    # os.makedirs('master/path1/path1.1/path1.1.1')
    # os.makedirs('nonmaster/path1/path1.1/path1.1.1')
    master.ensure_dir('master/path1/path1.1/path1.1.1')
    nonmaster.ensure_dir('nonmaster/path1/path1.1/path1.1.1')
    return os.path.abspath(str(master)), \
           os.path.abspath(str(nonmaster))



def test_find_master_dir(fake_master):
    """
    parent
        /master
            /servi
                \servi_templates
    """

    master, nonmaster = fake_master

    assert find_master_dir('master/servi/servi_templates') == master
    assert find_master_dir('master/servi') == master
    assert find_master_dir('master') == master

    with pytest.raises(MasterNotFound):
        find_master_dir(os.path.join(master, '..'))

    with pytest.raises(MasterNotFound):
        find_master_dir(nonmaster)
    assert find_master_dir(nonmaster, fail_ok=True) == None

    with pytest.raises(MasterNotFound):
        find_master_dir('/')

    print(MasterNotFound()) # for pytest coverage

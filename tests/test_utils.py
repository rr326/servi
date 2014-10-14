from servi.config import find_master_dir
from tests.fixtures import *
from servi.exceptions import MasterNotFound
from servi.command import process_and_run_command_line as servi_run
from time import sleep
from servi.utils import timeit
import sys
import io


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
    assert find_master_dir(nonmaster, fail_ok=True) is None

    with pytest.raises(MasterNotFound):
        find_master_dir('/')

    print(MasterNotFound())  # for pytest coverage


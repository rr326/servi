from servi.config import find_master_dir, find_ancestor_with
from servi.tests.fixtures import *
from contextlib import contextmanager


def test_find_up(fake_master):
    master_dir =  os.path.join(os.getcwd(), 'master')

    assert find_ancestor_with('master/servi/servi_templates', 'servi') == \
        master_dir
    assert find_ancestor_with('master/servi', 'servi') == master_dir
    assert find_ancestor_with('master', 'servi') == master_dir

    assert find_ancestor_with('nonmaster/anotherpath', 'servi') is None
    assert find_ancestor_with('nonmaster', 'servi') is None
    assert find_ancestor_with('.', 'servi') is None
    assert find_ancestor_with('/', 'servi') is None


@contextmanager
def allow_cwd_change():
    """
    This is useful if your code may change the working directory
    (possibly due to a raised error)
    """
    start_dir = os.getcwd()
    yield
    os.chdir(start_dir)


def test_find_master_dir(fake_master):
    """
    parent
        /master
            /servi
                \servi_templates
    """
    with allow_cwd_change():
        start_dir = os.getcwd()
        master_dir = os.path.abspath(os.path.join(os.getcwd(), 'master'))

        def assert_find_master(path):
            os.chdir(os.path.join(start_dir, path))
            retval = find_master_dir()
            assert retval == master_dir

        assert_find_master('master/servi/servi_templates')
        assert_find_master('master/servi')
        assert_find_master('master')

        with pytest.raises(MasterNotFound):
            assert_find_master('.')

        with pytest.raises(MasterNotFound):
            assert_find_master('nonmaster/anotherpath')

        with pytest.raises(MasterNotFound):
            assert_find_master('/')

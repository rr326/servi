from tests.fixtures import *
from servi.command import process_and_run_command_line as servi_run
from servi.exceptions import ServiError, ForceError


@pytest.mark.wip
def test_lans(setup_init, dirty_ignored_files):
    with pytest.raises(ServiError):
        servi_run('copy NONEXISTINGFILE')

    mod_file = dirty_ignored_files[0]
    with pytest.raises(ForceError):
        servi_run('copy ' + mod_file)

    assert servi_run('copy -f ' + mod_file)

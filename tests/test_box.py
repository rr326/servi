from tests.fixtures import *
from servi.utils import *
from servi.manifest import Manifest
from servi.template_mgr import TemplateManager
from servi.command import process_and_run_command_line as servi_run
from servi.commands.usebox import UseboxCommand
from servi.commands.buildbox import get_boxname, get_all_boxes
import servi.commands.buildbox as buildbox
from servi.exceptions import ServiError, ForceError
import subprocess
from datetime import datetime

@pytest.fixture()
def clean_boxes():
    for f in os.listdir(c.BOX_DIR):
        os.remove(os.path.join(c.BOX_DIR, f))


def test_get_all_boxes(clean_master, mock_template_dir, servi_init,
                       clean_boxes):

    boxlist = [
        'servi_box_3_4_11.box',
        'servi_box_1_1_12.box',
        'servi_box_1_1_1.box',
        'bogusfile',
    ]

    for f in boxlist:
        with open(os.path.join(c.BOX_DIR, f), 'w') as fp:
            fp.write('stuff')

    assert get_all_boxes()[0][0] == 'servi_box_3_4_11.box'
    assert len(get_all_boxes()) == 3

    os.remove(os.path.join(c.BOX_DIR, boxlist[0]))
    assert get_all_boxes()[0][0] == 'servi_box_1_1_12.box'

    os.remove(os.path.join(c.BOX_DIR, boxlist[1]))
    assert get_all_boxes()[0][0] == 'servi_box_1_1_1.box'

    os.remove(os.path.join(c.BOX_DIR, boxlist[2]))
    assert get_all_boxes() == []


def test_build_box(clean_master, mock_template_dir, servi_init, clean_boxes):
    assert servi_run('buildbox --mock')

    # Now that it already exists
    assert servi_run('buildbox --mock') == buildbox.SKIPPED


def test_use_box(clean_master, mock_template_dir, servi_init, clean_boxes):
    with pytest.raises(ServiError):
        assert servi_run('usebox --mock')

    with open(os.path.join(c.BOX_DIR, 'servi_box_0_0_0.box'), 'w') as fp:
        fp.write('MOCKED BOX')

    with pytest.raises(ForceError):
        assert servi_run('usebox --mock')

    assert servi_run('usebox --force --mock')


@pytest.mark.slow_test
def test_build_and_use(clean_master, mock_template_dir, clean_boxes, tmpdir):
    """
    This takes a LONG time. (10min?)
    Run with py.test -m 'slow_test' -s -x
    """
    with timeit():
        with reset_cwd():
            projdir = tmpdir.mkdir('myproject')
            projdir.chdir()
            assert servi_run('init .')
            assert servi_run('buildbox')
            assert servi_run('usebox')
            status_text = subprocess.check_output('vagrant status', shell=True)
            status_text = status_text.decode(encoding='ascii', errors='ignore')
            assert re.search('default\s*running',status_text)
            subprocess.call('vagrant destroy -f', shell=True)

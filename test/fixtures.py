import os
from datetime import datetime
import shutil
import re
import pytest
import config
import config as c
from commands.utils.utils import *
import subprocess
from commands.utils.template_mgr import TemplateManager, BACKUP_PREFIX
import tempfile

def confirm_proper_directory():
    assert os.path.abspath(os.getcwd()) == os.path.abspath(c.MASTER_DIR)


@pytest.fixture()
def clean_master():
    """
    Clean the master directory, making it empty.
    (Exclude the servi directory and anything named BACKUP_PREFIX*)
    """
    print('clean_master()')
    confirm_proper_directory()
    timestamp = datetime.utcnow()

    for path in os.listdir(c.MASTER_DIR):
        if re.match('({0}.*|servi$)'.format(BACKUP_PREFIX), path):
            print('ignoring: {0}'.format(path))
            continue
        TemplateManager.rename_master_file_static(path, timestamp)


@pytest.fixture()
def servi_init():
    # use the --template_dir so that you can pass a monkeypatched TEMPLATE_DIR
    # (such as from mock_template_dir) to the new process
    subprocess.call('python servi --template_dir {0} init'.format(c.TEMPLATE_DIR), shell=True)


def modify_file(fname):
    """
    This will add, change, and remove some lines in a file
    Note - it does NOT do this intelligently. So a .json file will no longer
    be correct.
    """

    with open(fname, 'r') as fp:
        lines = fp.readlines()

    # delete line 2
    if len(lines) > 3:
        lines = lines[0:1] + (lines[2:])

    # Add to end
    lines.append('Here\nare\nsome\nnew\nlines\nat\nthe end of the file\n')

    # Modify in middle
    mid = len(lines) // 2
    oldline = lines[mid]
    newline = oldline[0:len(oldline)//2] + 'HERE IS SOME NEW TEXT' + \
        oldline[len(oldline)//2 + 1:]
    lines[mid] = newline

    # Now write the lines
    with open(fname, 'w') as fp:
        fp.writelines(lines)


@pytest.fixture()
def dirty_master():
    modify_file(pathfor('Vagrantfile', c.MASTER))


@pytest.fixture()
def dirty_ignored_files():
    modify_file(
        pathfor('ansible_config/roles/projectSpecific/tasks/main.yml', c.MASTER))
    os.remove(pathfor("apache_config/sites-available/THISSITE.conf", c.MASTER))


# To simplify translating Linux process error codes into asserts
def process_failed(exit_code):
    return exit_code != 0


def process_succeeded(exit_code):
    return exit_code == 0

@pytest.fixture()
def mock_template_dir(monkeypatch):
    """
    Copy TEMPLATE_DIR to a tmp directory
    Set TEMPLATE_DIR enviornment variable to the new dir
    (config.py will override TEMPLATE_DIR based on the env variable)
    """
    print('in mock_template_dir')
    temp_dir = tempfile.mkdtemp(prefix='_tmp_', dir='.')
    temp_dir = os.path.join(temp_dir, 'templates')
    shutil.copytree(c.TEMPLATE_DIR, temp_dir)
    monkeypatch.setattr(c, 'TEMPLATE_DIR', temp_dir)
    print('mock_template_dir - c.TEMPLATE_DIR: ', c.TEMPLATE_DIR)

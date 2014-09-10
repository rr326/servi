import os
from datetime import datetime
import shutil
import re
import pytest
from config import *
from commands.utils.utils import *
import subprocess

BACKUP_PREFIX = '_OLD'

def confirm_proper_directory():
    assert os.path.abspath(os.getcwd()) == os.path.abspath(MASTER_DIR)


@pytest.fixture()
def clean_master():
    """
    Clean the master directory, making it empty.
    (Exclude the servi directory and anything named _SAVEDxxx)
    """
    confirm_proper_directory()

    tomove = []
    for path in os.listdir(MASTER_DIR):
        if re.match('({0}.*|servi$)'.format(BACKUP_PREFIX), path):
            print('ignoring: {0}'.format(path))
            continue
        tomove.append(path)

    if tomove:
        backupdir = '{0}_{1}'.format(BACKUP_PREFIX,
                                     datetime.utcnow().isoformat())
        os.mkdir(backupdir)
        for path in tomove:
            print('backing up: {0}'.format(path))
            shutil.move(path, backupdir)


@pytest.fixture()
def servi_init():
    subprocess.call('python servi init', shell=True)


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
    modify_file(pathfor('Vagrantfile', MASTER))
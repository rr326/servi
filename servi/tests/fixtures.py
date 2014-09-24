from datetime import datetime
import shutil
import re
import tempfile

import pytest

from servi_utils import *

from template_mgr import BACKUP_PREFIX
from command import process_and_run_command_line as servi_run


@pytest.fixture()
def clean_master():
    """
    Clean the master directory, making it empty.
    (Exclude the servi directory and anything named BACKUP_PREFIX*)
    Note - this will NOT backup the master directory. You should do that
    with conftest.py with 'backup_master() autouse/session
    """
    print('clean_master()')
    for path in os.listdir(c.MASTER_DIR):
        if re.match('({0}.*|servi$)'.format(BACKUP_PREFIX), path):
            print('ignoring: {0}'.format(path))
            continue
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@pytest.fixture()
def servi_init():
    # use the --template_dir so that you can pass a monkeypatched MSTR_TMPL_DIR
    # (such as from mock_template_dir) to the new process
    servi_run('--template_dir {0} init'.format(c.MSTR_TMPL_DIR))


def modify_file(fname):
    """
    This will add, change, and remove some lines in a file
    Note - it does NOT do this intelligently. So a .json file will no longer
    be correct.
    """
    if re.search('.*\.yml', fname, flags=re.IGNORECASE):
        # yaml - modify in a safe way
        modify_yaml(fname)
        return

    with open(fname, 'r') as fp:
        lines = fp.readlines()

    # delete line 2
    if len(lines) > 3:
        lines = lines[0:1] + (lines[2:])

    # Add to end
    lines.append('#Here\nare\nsome\nnew\nlines\nat\nthe end of the file\n')
    lines.append('#'+datetime.utcnow().isoformat())

    # Modify in middle
    mid = len(lines) // 2
    oldline = lines[mid]
    newline = oldline[0:len(oldline)//2] + 'HERE IS SOME NEW TEXT' + \
        oldline[len(oldline)//2 + 1:]
    lines[mid] = newline

    # Now write the lines
    with open(fname, 'w') as fp:
        fp.writelines(lines)


def modify_yaml(fname):
    with open(fname, 'a') as fp:
        fp.write('\n# HERE IS SOME NEW TEXT: {0}'
                 .format(datetime.utcnow().isoformat()))


@pytest.fixture()
def dirty_master():
    modify_file(pathfor('Vagrantfile', c.MASTER))


@pytest.fixture()
def dirty_ignored_files():
    modify_file(
        pathfor('ansible_config/roles/projectSpecific/tasks/main.yml',
                c.MASTER))
    os.remove(pathfor("apache_config/sites-available/THISSITE.conf", c.MASTER))


# To simplify translating Linux process error codes into asserts
def process_failed(exit_code):
    return exit_code != 0


def process_succeeded(exit_code):
    return exit_code == 0


@pytest.fixture()
def mock_template_dir(monkeypatch):
    """
    Copy MSTR_TMPL_DIR to a tmp directory
    Set MSTR_TMPL_DIR enviornment variable to the new dir
    (config.py will override MSTR_TMPL_DIR based on the env variable)
    """
    # TODO - Is there a less hacky way to do set the template_dir?

    print('in mock_template_dir')
    temp_dir = tempfile.mkdtemp(prefix='_tmp_', dir='.')
    temp_dir = os.path.join(temp_dir, 'templates')
    shutil.copytree(c.MSTR_TMPL_DIR, temp_dir)
    monkeypatch.setattr(c, 'MSTR_TMPL_DIR', temp_dir)
    print('mock_template_dir - c.MSTR_TMPL_DIR: ', c.MSTR_TMPL_DIR)


@pytest.fixture()
def dirty_template(monkeypatch):
    mock_template_dir(monkeypatch)
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.TEMPLATE))


@pytest.fixture()
def dirty_template_and_master(monkeypatch):
    mock_template_dir(monkeypatch)
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.TEMPLATE))
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.MASTER))

#
# New, simplified test scenarios
#


@pytest.fixture()
def synced_file_template_dirty(monkeypatch):
    clean_master()
    mock_template_dir(monkeypatch)
    servi_init()
    modify_file(pathfor('Vagrantfile', c.TEMPLATE))


@pytest.fixture()
def synced_file_template_and_master_dirty(monkeypatch):
    clean_master()
    mock_template_dir(monkeypatch)
    servi_init()
    modify_file(pathfor('Vagrantfile', c.TEMPLATE))
    modify_file(pathfor('Vagrantfile', c.MASTER))


@pytest.fixture()
def template_only_unused_role(monkeypatch):
    clean_master()
    mock_template_dir(monkeypatch)
    servi_init()
    shutil.copytree(pathfor('ansible_config/roles/baseUbuntu', c.TEMPLATE),
                    pathfor('ansible_config/roles/UnusedRole', c.TEMPLATE))


@pytest.fixture()
def master_only():
    clean_master()
    servi_init()
    shutil.copy2(pathfor('Vagrantfile', c.MASTER),
                 pathfor('myscript.py', c.MASTER))


@pytest.fixture()
def template_but_ignored(monkeypatch):
    clean_master()
    mock_template_dir(monkeypatch)
    servi_init()
    modify_file(pathfor('apache_config/sites-available/THISSITE.conf',
                c.TEMPLATE))

@pytest.fixture(scope='session')
def fake_master():
    """
    parent
        /master
            /servi
                \servi_templates
    """
    temp_dir = tempfile.mkdtemp(prefix='_tmp_')
    os.chdir(temp_dir)
    os.makedirs('master/servi/servi_templates')
    os.makedirs('nonmaster/anotherpath')





"""
Scenarios
* No master
* Changed master or template:
    * Synced file: In Template and Master (eg: Vagrantfile)
    * Template_only: eg: UnusedRole (mongo)
    * Master_only: eg: myscript.sh
    * Template_but_ignored: eg: THISSFILE.conf, ansible_config/playbook.yml
    * [skipping] Ignored_Entirely: servi_data.json, VERSION_FILE.json
"""

from datetime import datetime
import shutil
import re
import tempfile
import os
import pytest
from servi.utils import *
from servi.template_mgr import BACKUP_PREFIX
from servi.command import process_and_run_command_line as servi_run
from servi.manifest import Manifest


#
# Initialize a temporary dirctory for all fixture use






@pytest.fixture()
def clean_master(monkeypatch, tmpdir):
    temp_dir = tmpdir.mkdir('serviplate')
    monkeypatch.setattr(c, 'MASTER_DIR', str(temp_dir))
    os.chdir(c.MASTER_DIR)
    print('clean_master: c.MASTER_DIR {0}'.format(c.MASTER_DIR))

@pytest.fixture()
def mock_template_dir(monkeypatch):
    """
    Copy TMPL_DIR_SITE to a tmp directory
    Set TMPL_DIR_SITE enviornment variable to the new dir
    (config.py will override TMPL_DIR_SITE based on the env variable)
    """

    print('in mock_template_dir')
    temp_dir = tempfile.mkdtemp(prefix='_tmp_', dir='.')
    temp_dir = os.path.abspath(os.path.join(temp_dir, 'templates'))
    shutil.copytree(c.TMPL_DIR_SITE, temp_dir)
    monkeypatch.setattr(c, 'TMPL_DIR_SITE', temp_dir)
    print('mock_template_dir - c.TMPL_DIR_SITE: ', c.TMPL_DIR_SITE)

@pytest.fixture()
def setup_empty(clean_master, mock_template_dir):
    return

@pytest.fixture()
def setup_init(clean_master, mock_template_dir):
    servi_run('--template_dir {0} init .'.format(c.TMPL_DIR_SITE))
    m0 = Manifest(c.MASTER)
    return {"m0": m0}




@pytest.fixture()
def servi_init():
    # use the --template_dir so that you can pass a monkeypatched TMPL_DIR_SITE
    # (such as from mock_template_dir) to the new process
    servi_run('--template_dir {0} init .'.format(c.TMPL_DIR_SITE))
    m0 = Manifest(c.MASTER)
    return {"m0": m0}


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
def dirty_template(setup_empty):
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.TEMPLATE))


@pytest.fixture()
def dirty_template_and_master(setup_empty):
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.TEMPLATE))
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.MASTER))

#
# New, simplified test scenarios
#


@pytest.fixture()
def synced_file_template_dirty(setup_init):
    modify_file(pathfor('Vagrantfile', c.TEMPLATE))
    return {"m0": setup_init["m0"]}


@pytest.fixture()
def synced_file_template_and_master_dirty(setup_init):
    modify_file(pathfor('Vagrantfile', c.TEMPLATE))
    modify_file(pathfor('Vagrantfile', c.MASTER))
    return {"m0": setup_init["m0"]}

@pytest.fixture()
def template_only_unused_role(setup_init):
    shutil.copytree(pathfor('ansible_config/roles/baseUbuntu', c.TEMPLATE),
                    pathfor('ansible_config/roles/UnusedRole', c.TEMPLATE))

    return {"m0": setup_init["m0"]}


@pytest.fixture()
def master_only(setup_init):
    shutil.copy2(pathfor('Vagrantfile', c.MASTER),
                 pathfor('myscript.py', c.MASTER))
    return {"m0": setup_init["m0"]}

@pytest.fixture()
def template_but_ignored(setup_init):
    modify_file(pathfor('apache_config/sites-available/THISSITE.conf',
                c.TEMPLATE))
    return {"m0": setup_init["m0"]}







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

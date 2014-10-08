import pytest
from tests.fixtures import *
from servi.manifest import Manifest
import servi.config as c
from servi.command import process_and_run_command_line as servi_run
import os


@pytest.fixture
def mock_ansible_inventory():
    inv_path = os.path.join(
        c.MASTER_DIR, '.vagrant/provisioners/ansible/inventory')
    inv_file = os.path.join(inv_path, 'vagrant_ansible_inventory')

    os.makedirs(inv_path)

    with open(inv_file, "w") as fp:
        fp.write("default ansible_ssh_host=127.0.0.1 ansible_ssh_port=2222")


def test_lans(clean_master, mock_template_dir, servi_init,
              mock_ansible_inventory):
    # -C check (~ 3 seconds), --syntax_check (~5s)
    assert servi_run('lans --syntax-check')

    # Might need to remove since tests won't all have vagrant up
    assert servi_run('lans -p -C')

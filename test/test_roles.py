from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run




ROLETEST_PLAYBOOK = '''
---
-   hosts: all
    vars_files:
      - ../servi_config.yml
    sudo: yes
    tasks:
    roles:
        # - baseUbuntu
        #mainAccount
        - hardenedUbuntu
        - hardenedApache
        - projectSpecific
'''


def test_role_handling(clean_master, servi_init, mock_template_dir, capsys):
    # Role in master, not in template directory -- ignored

    # Role commented in master and also in template:
    # 1) don't copy
    # 2) Do warn
    with open(pathfor('ansible_config/playbook.yml', c.MASTER), 'w') as fp:
        fp.write(ROLETEST_PLAYBOOK)
    modify_file(pathfor('ansible_config/roles/baseUbuntu/tasks/main.yml',
                c.TEMPLATE))
    modify_file(pathfor('ansible_config/roles/mainAccount/tasks/main.yml',
                c.TEMPLATE))

    assert servi_run('update')

    tmgr = TemplateManager()
    assert tmgr.possible_roles == {'baseUbuntu', 'mainAccount'}
    assert tmgr.modified_possible_roles == {'baseUbuntu', 'mainAccount'}
    assert 'ansible_config/playbook.yml' in tmgr.changed_but_ignored_files


    # TODO - make sure a new role file is also caught
    # TODO ? - switch to using raw_template_playbook ? (like test_template_manager)
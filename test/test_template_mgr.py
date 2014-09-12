from commands.utils.template_mgr import *
from test.fixtures import *
import pytest
import tempfile


pytestmark = pytest.mark.wip

PLAYBOOK_TESTDATA = '''
---
-   hosts: all
    vars_files:
      - ../servi_config.yml
    sudo: yes
    tasks:
    roles:
        #- baseUbuntu
         #mainAccount
 #       - hardenedUbuntu
        - hardenedApache
        - projectSpecific
        - HERE_IS_A_DIFFERENT_ROLE



'''
TEMPLATE_ROLES = {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu',
                  'mainAccount', 'projectSpecific'}

# Do fixtures once for module
clean_master()
servi_init()
tmgr = TemplateManager


def test_get_template_roles():
    res = tmgr._get_template_roles()
    print(res)
    assert len(res) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= set(res)


def test_get_master_roles1():
    roles, possible_roles = tmgr._get_master_roles(TEMPLATE_ROLES)
    print('roles: ', roles)
    print('possible_roles: ', possible_roles)
    assert len(roles) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= roles
    assert type(possible_roles) is set


def test_get_master_roles2():
    roles, possible_roles = tmgr._get_master_roles(
        TEMPLATE_ROLES, test_raw = PLAYBOOK_TESTDATA)
    print('roles: ', roles)
    print('possible_roles: ', possible_roles)
    assert roles == {'hardenedApache', 'projectSpecific',
                     'HERE_IS_A_DIFFERENT_ROLE'}
    assert possible_roles == {'baseUbuntu', 'mainAccount', 'hardenedUbuntu'}


def test_role_of_fname():

    assert tmgr._role_of_fname(
        'ansible_config/roles/mainAccount/tasks/main.yml') == 'mainAccount'

    assert tmgr._role_of_fname('ansible_config/roles/mainAccount') \
           == 'mainAccount'

    assert tmgr._role_of_fname('apache_config/sites-available/THISSITE') \
           is None


def test_mock(mock_template_dir):
    assert not subprocess.call('python servi init', shell=True)
    assert 0
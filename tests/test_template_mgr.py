from servi.template_mgr import *
from tests.fixtures import *


PLAYBOOK_TESTDATA = '''
---
-   hosts: all
    vars_files:
      - ../Servifile.yml
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


@pytest.fixture()
def template_manager_setup(setup_init):
    tmgr = TemplateManager()
    return tmgr


def test_get_template_roles(template_manager_setup):
    res = template_manager_setup.roles
    print(res)
    assert len(res) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= set(res)


def test_get_master_roles1(template_manager_setup):
    tmgr = template_manager_setup
    print('roles: ', tmgr.roles)
    print('possible_roles: ', tmgr.possible_roles)
    assert len(tmgr.roles) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= tmgr.roles
    assert type(tmgr.possible_roles) is set


def test_get_master_roles2(template_manager_setup):
    tmgr = TemplateManager(raw_template_playbook=PLAYBOOK_TESTDATA)
    print('roles: ', tmgr.roles)
    print('possible_roles: ', tmgr.possible_roles)
    assert tmgr.roles == {'hardenedApache', 'projectSpecific',
                          'HERE_IS_A_DIFFERENT_ROLE'}
    assert tmgr.possible_roles == {'baseUbuntu', 'mainAccount',
                                   'hardenedUbuntu'}


def test_role_of_fname(template_manager_setup):
    tmgr = template_manager_setup
    assert tmgr.role_of_fname(
        'ansible_config/roles/mainAccount/tasks/main.yml') == 'mainAccount'

    assert tmgr.role_of_fname('ansible_config/roles/mainAccount') \
        == 'mainAccount'

    assert tmgr.role_of_fname('apache_config/sites-available/mysite') \
        is None


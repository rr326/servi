from commands.utils.template_mgr import *
from test.fixtures import *


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
tmgr = TemplateManager()


def test_get_template_roles():
    res = tmgr.roles
    print(res)
    assert len(res) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= set(res)


def test_get_master_roles1():
    print('roles: ', tmgr.roles)
    print('possible_roles: ', tmgr.possible_roles)
    assert len(tmgr.roles) >= 5
    assert {'baseUbuntu', 'hardenedApache', 'hardenedUbuntu', 'mainAccount',
            'projectSpecific'} <= tmgr.roles
    assert type(tmgr.possible_roles) is set


def test_get_master_roles2():
    tmgr = TemplateManager(raw_template_playbook=PLAYBOOK_TESTDATA)
    print('roles: ', tmgr.roles)
    print('possible_roles: ', tmgr.possible_roles)
    assert tmgr.roles == {'hardenedApache', 'projectSpecific',
                          'HERE_IS_A_DIFFERENT_ROLE'}
    assert tmgr.possible_roles == {'baseUbuntu', 'mainAccount',
                                   'hardenedUbuntu'}


def test_role_of_fname():

    assert tmgr.role_of_fname(
        'ansible_config/roles/mainAccount/tasks/main.yml') == 'mainAccount'

    assert tmgr.role_of_fname('ansible_config/roles/mainAccount') \
        == 'mainAccount'

    assert tmgr.role_of_fname('apache_config/sites-available/THISSITE') \
        is None


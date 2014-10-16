from tests.fixtures import *
from servi.utils import *
from servi.manifest import Manifest
from servi.template_mgr import TemplateManager
from servi.command import process_and_run_command_line as servi_run


def test_diff(setup_init):
    m0 = setup_init["m0"]

    # Unused Role
    shutil.copytree(pathfor('ansible_config/roles/baseUbuntu', c.TEMPLATE),
                    pathfor('ansible_config/roles/UnusedRole', c.TEMPLATE))

    mod_templates = ['Vagrantfile',
                     'apache_config/sites-available/mysite.conf',
                     'ansible_config/playbook.yml']

    mod_master = ['Vagrantfile',
                  'ansible_config/playbook.yml']

    del_master = ['apache_config/sites-available/mysite.conf']

    for file in mod_templates:
        modify_file(pathfor(file, c.TEMPLATE))

    for file in mod_master:
        modify_file(pathfor(file, c.MASTER))

    for file in del_master:
        os.remove(pathfor(file, c.MASTER))

    m1 = Manifest(c.MASTER)

    added, changed, removed = Manifest.diff_files(m1, m0)

    assert added == set()
    assert changed == {'Vagrantfile', 'ansible_config/playbook.yml'}
    assert removed == {'apache_config/sites-available/mysite.conf'}

    tmgr = TemplateManager()
    assert tmgr.t_added == set()
    assert tmgr.t_changed == {'Vagrantfile', 'ansible_config/playbook.yml'}
    # Also UnusedRole stuff
    assert tmgr.t_removed >= \
        {'apache_config/sites-available/mysite.conf'}
    assert tmgr.t_mod_but_ignored == {
        'apache_config/sites-available/mysite.conf',
        'ansible_config/playbook.yml'}

    assert servi_run('diff')


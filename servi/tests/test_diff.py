from tests.fixtures import *
from commands.utils.servi_utils import *
from commands.utils.manifest import Manifest
from commands.utils.template_mgr import TemplateManager


def test_diff(clean_master, mock_template_dir, servi_init):
    m0 = Manifest(c.TEMPLATE)

    # Unused Role
    shutil.copytree(pathfor('ansible_config/roles/baseUbuntu', c.TEMPLATE),
                    pathfor('ansible_config/roles/UnusedRole', c.TEMPLATE))

    mod_templates = ['Vagrantfile',
                     'apache_config/sites-available/THISSITE.conf',
                     'ansible_config/playbook.yml']

    mod_master = ['Vagrantfile',
                  'ansible_config/playbook.yml']

    del_master = ['apache_config/sites-available/THISSITE.conf']

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
    assert removed == {'apache_config/sites-available/THISSITE.conf'}

    tmgr = TemplateManager()
    assert tmgr.added_files == set()
    assert tmgr.changed_files == {'Vagrantfile', 'ansible_config/playbook.yml'}
    # Also UnusedRole stuff
    assert tmgr.removed_files >= \
        {'apache_config/sites-available/THISSITE.conf'}
    assert tmgr.changed_but_ignored_files == {
        'apache_config/sites-available/THISSITE.conf',
        'ansible_config/playbook.yml'}


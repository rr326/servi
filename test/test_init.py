from test.fixtures import *
import pytest
from commands.utils.manifest import Manifest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run

class TestInit():

    def test_clean(self, clean_master):
        # init on a clean directory should work
        m0 = Manifest(c.MASTER)
        assert servi_run('init')
        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == set()
        assert removed == set()
        assert len(added) > 10

    def test_synced_file_template_dirty(self, synced_file_template_dirty):
        m0 = Manifest(c.MASTER)
        with pytest.raises(ForceError):
            servi_run('init')

        assert servi_run('init -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'Vagrantfile'}

    def test_synced_file_template_and_master_dirty(
            self, synced_file_template_and_master_dirty):
        m0 = Manifest(c.MASTER)

        with pytest.raises(ForceError):
            servi_run('init')

        assert servi_run('init -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'Vagrantfile'}

    def test_template_only_unused_role(self, template_only_unused_role):
        m0 = Manifest(c.MASTER)
        assert servi_run('init')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()


    def test_master_only(self, master_only):
        m0 = Manifest(c.MASTER)
        assert servi_run('init')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_template_but_ignored(self, template_but_ignored):
        m0 = Manifest(c.MASTER)

        with pytest.raises(ForceError):
            servi_run('init')

        assert servi_run('init -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'apache_config/sites-available/THISSITE.conf'}
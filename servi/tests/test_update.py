from tests.fixtures import *
import pytest
from commands.utils.manifest import Manifest
from commands.utils.utils import *
from command import process_and_run_command_line as servi_run
from servi_exceptions import *


class TestUpdate():

    def test_clean(self, clean_master, servi_init):
        # init on a clean directory should work
        m0 = Manifest(c.MASTER)
        assert servi_run('update')
        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_synced_file_template_dirty(self, synced_file_template_dirty):
        m0 = Manifest(c.MASTER)

        assert servi_run('update')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'Vagrantfile'}

    def test_synced_file_template_and_master_dirty(
            self, synced_file_template_and_master_dirty):
        with pytest.raises(ServiError):
            servi_run('update')

    def test_template_only_unused_role(self, template_only_unused_role):
        m0 = Manifest(c.MASTER)
        assert servi_run('update')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_master_only(self, master_only):
        m0 = Manifest(c.MASTER)
        assert servi_run('update')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_template_but_ignored(self, template_but_ignored):
        m0 = Manifest(c.MASTER)

        assert servi_run('update')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert  added | changed | removed == set()
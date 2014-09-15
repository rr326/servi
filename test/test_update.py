from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run

@pytest.mark.wip
class TestInit():

    def test_clean(self, clean_master):
        with pytest.raises(ServiError):
            assert servi_run('update')
        servi_run('init')
        assert servi_run('update')

    def test_synced_file_template_dirty(self, synced_file_template_dirty):
        assert servi_run('update')

    def test_synced_file_template_and_master_dirty(
            self, synced_file_template_and_master_dirty):
        with pytest.raises(ServiError):
            servi_run('update')

    def test_template_only_unused_role(self, template_only_unused_role):
        assert servi_run('update')

    def test_master_only(self, master_only):
        assert servi_run('update')

    def test_template_but_ignored(self, template_but_ignored):
        assert servi_run('update')
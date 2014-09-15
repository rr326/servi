from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run




def test_clean(clean_master, servi_init):
    # init on a clean directory should work
    assert servi_run('init')

    # Update on a clean directory should work too
    assert servi_run('update')

    tmgr = TemplateManager()
    assert tmgr.added_files | tmgr.changed_files | tmgr.removed_files == set()

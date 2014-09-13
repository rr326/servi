from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run


DIFF_SUMMARY = \
    """Diff of servi template and existing MASTER dir.
===============================================
Template Directory: /Users/rrosen/dev/serviplate/servi/templates
Master Directory:   /Users/rrosen/dev/serviplate

Changed files:
===============
(no changed files)

Removed (Template files not found in Master):
=============================================
	TEMPLATE_VERSION.json [on "ignore" list]

Added (to master and not in template):
======================================
	(NOT SHOWN)"""

def test_clean(clean_master, servi_init):
    # init on a clean directory should work
    assert servi_run('init')

    # Update on a clean directory should work too
    assert servi_run('update')

    # Diff should show no surprising changes
    output = subprocess.check_output(
        'python servi diff --difftool "git diff"',
        shell=True,
        universal_newlines=True)

    output = str(output)
    assert DIFF_SUMMARY in output
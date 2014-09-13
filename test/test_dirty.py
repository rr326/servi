from test.fixtures import *
import pytest
import commands.utils.manifest as mfest
from commands.utils.utils import *
import subprocess
import re
from command import process_and_run_command_line as servi_run

# noinspection PyPep8
DIFF_SUMMARY = \
    """Diff of servi template and existing MASTER dir.
===============================================
Template Directory: /Users/rrosen/dev/serviplate/servi/templates
Master Directory:   /Users/rrosen/dev/serviplate

Changed files:
===============
	ansible_config/roles/projectSpecific/tasks/main.yml [on "ignore" list]

Removed (Template files not found in Master):
=============================================
	TEMPLATE_VERSION.json [on "ignore" list]
	apache_config/sites-available/THISSITE.conf [on "ignore" list]

Added (to master and not in template):
======================================
	(NOT SHOWN)"""

DIFF_END = \
    """-Here
-are
-some
-new
-lines
-at
-the end of the file
"""


def test_dirty(clean_master, servi_init, dirty_master):
    # init should fail (since Master has been updated)
    assert not servi_run('init')

    # update should also fail
    assert not servi_run('update')

    # init -f should succeed (force)
    assert servi_run('init -f')


def test_init_dirty_ignore(clean_master, servi_init, dirty_ignored_files):
    # Should fail - init does't ignore
    assert not servi_run('init')


def test_update_dirty_ignore(clean_master, servi_init, dirty_ignored_files):
    # Should succeed since ignored files
    assert servi_run('update')


def test_diff(clean_master, servi_init, dirty_ignored_files):
    output = subprocess.check_output('python servi diff --difftool "git diff"',
                                     shell=True,
                                     universal_newlines=True)
    output = str(output)

    assert DIFF_SUMMARY in output
    assert re.search('-.*HERE IS SOME NEW TEXT', output)
    assert DIFF_END in output

from servi.tests.fixtures import *
import pytest
import os
import subprocess as sp
import servi.config as c
from servi.command import process_and_run_command_line as servi_run

def test_servi_shellscript(tmpdir):
    tempdir = str(tmpdir.mkdir('serviplate'))
    os.chdir(tempdir)
    os.makedirs(os.path.join(tempdir, 'path1/path1.1/path1.1.1'))
    print('cwd: {0}'.format(os.getcwd()))
    assert servi_run('init .')

    shell_cmd = 'servi'

    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=os.path.join(tempdir, 'path1/path1.1/path1.1.1'))
    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=os.path.join(tempdir, 'path1/path1.1'))
    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=os.path.join(tempdir, 'path1'))
    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=os.path.join(tempdir, '.'))

    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=os.path.join(tempdir, '..'))
    assert not sp.call(
        [shell_cmd, 'update', '--help'],
        cwd=tempdir)


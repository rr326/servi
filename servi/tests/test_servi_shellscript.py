from servi.tests.fixtures import *
import pytest
import os
import subprocess as sp
import servi.config as c


def test_servi_shellscript():
    print('cwd: {0}'.format(os.getcwd()))
    shell_cmd = os.path.join(c.SERVI_DIR, 'bin/servi')
    print('SHELL_CMD: {0}'.format(shell_cmd))

    assert not sp.call([shell_cmd, '--help'],
                       cwd=os.path.join(c.SERVI_DIR, 'servi/commands/utils'))
    assert not sp.call([shell_cmd, '--help'],
                       cwd=os.path.join(c.SERVI_DIR, 'servi/commands/'))
    assert not sp.call([shell_cmd, '--help'],
                       cwd=os.path.join(c.SERVI_DIR, 'servi'))
    assert not sp.call([shell_cmd, '--help'],
                       cwd=os.path.join(c.SERVI_DIR, '.'))
    assert not sp.call([shell_cmd, '--help'],
                       cwd=os.path.join(c.SERVI_DIR, '..'))

    assert sp.call([shell_cmd, '--help'],
                   cwd=os.path.join(c.SERVI_DIR, '../..'))
    assert sp.call([shell_cmd, '--help'], cwd='/')


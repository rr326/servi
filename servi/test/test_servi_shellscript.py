from test.fixtures import *
import pytest
import os
import subprocess as sp
import config as c

@pytest.mark.wip
def test_servi_shellscript():
    print('cwd: {0}'.format(os.getcwd()))
    SHELL_CMD=os.path.join(c.SERVI_DIR, 'bin/servi')
    print('SHELL_CMD: {0}'.format(SHELL_CMD))

    assert not sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'servi/commands/utils'))
    assert not sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'servi/commands/'))
    assert not sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'servi'))
    assert not sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'.'))
    assert not sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'..'))

    assert sp.call([SHELL_CMD,'--help'], cwd=os.path.join(c.SERVI_DIR,'../..'))
    assert sp.call([SHELL_CMD, '--help'], cwd='/')


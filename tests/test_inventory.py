from servi.config import find_master_dir
from tests.fixtures import *
from servi.exceptions import MasterNotFound
from servi.command import process_and_run_command_line as servi_run
from time import sleep
from servi.utils import timeit
import sys
import io
import json
import yaml

GOOD_REC = \
"""
---
HOSTS:
  prod:
    hosts:
      - prod.k2company.com
    vars:
        HOST_NAME: prod5.k2company.com,
        SERVER_NAME: prod.k2company.com
  stage:
    hosts:
      - stage.k2company.com
    vars:
        HOST_NAME: prod5.k2company.com,
        SERVER_NAME: stage.k2company.com
"""

BAD_REC = \
"""
---
HOSTS:
  prod:
    - hosts:
      - prod.k2company.com
    - vars:
        HOST_NAME: prod5.k2company.com,
        SERVER_NAME: prod.k2company.com
  stage:
    hosts: stage.k2company.com
    vars:
        - HOST_NAME: prod5.k2company.com,
        - SERVER_NAME: stage.k2company.com
  other:
    hosts:
      - stage.k2company.com
    VARS:
        HOST_NAME: prod5.k2company.com,
        SERVER_NAME: stage.k2company.com
"""

def equal_jsons(text1, text2):
    try:
        o1 = json.loads(text1.strip('\n\s"'))
        o2 = json.loads(text2.strip('\n\s"'))
    except ValueError:
        return False

    return o1 == o2

@pytest.mark.wip
def test_inventory(mock_homedir, setup_init):
    with open(c.SERVIFILE_GLOBAL_FULL, 'w') as fp:
        fp.write(BAD_REC)
    assert not servi_run('inventory')

    with open(c.SERVIFILE_GLOBAL_FULL, 'w') as fp:
        fp.write(GOOD_REC)
    assert not servi_run('inventory')
    good_o = yaml.load(GOOD_REC)['HOSTS']
    good_j = json.dumps(good_o)
    assert equal_jsons(servi_run('inventory --list'), good_j)
    assert equal_jsons(servi_run('inventory --host prod'),
                       json.dumps(good_o["prod"]))
    assert equal_jsons(servi_run('inventory --host MISSING'), json.dumps('{}'))


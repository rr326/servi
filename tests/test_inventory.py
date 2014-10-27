import json

import yaml

from tests.fixtures import *
from servi.command import process_and_run_command_line as servi_run


GOOD_REC = """
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

BAD_REC = """
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

SERVIFILE_LOCAL = """
---
HOSTS:
  vagrant:
      hosts:
        - 127.0.0.1
      vars:
          HOST_NAME: vagrant-mysite
          SERVER_NAME: vagrant-mysite
          IS_VAGRANT: True
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

    with open(pathfor(c.SERVIFILE, c.MASTER), 'w') as fp:
        fp.write(SERVIFILE_LOCAL)

    assert not servi_run('inventory')
    good_o = yaml.load(GOOD_REC)['HOSTS']
    servifile_o = yaml.load(SERVIFILE_LOCAL)['HOSTS']
    good_o = c.deep_update(good_o, servifile_o)

    good_j = json.dumps(good_o)
    assert equal_jsons(servi_run('inventory --list'), good_j)
    assert equal_jsons(servi_run('inventory --host prod'),
                       json.dumps(good_o["prod"]))
    assert equal_jsons(servi_run('inventory --host MISSING'), json.dumps('{}'))


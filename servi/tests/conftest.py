from datetime import datetime
import re
import os

import pytest

from template_mgr import TemplateManager, BACKUP_PREFIX
import config as c


@pytest.fixture(scope="session", autouse=True)
def backup_master():
    # Automatically do, but only once per session
    # Note - other _BACKUPS might be made by init or update.
    print('-'*200)
    print('backing up master')
    print('-'*200)
    print('\n\n')

    timestamp = datetime.utcnow()
    for path in os.listdir(c.MASTER_DIR):
        if re.match('({0}.*|servi$)'.format(BACKUP_PREFIX), path):
            print('ignoring: {0}'.format(path))
            continue
        TemplateManager.rename_master_file(path, timestamp)
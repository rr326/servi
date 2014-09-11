import shutil
import json
import os
import hashlib
import re
from datetime import datetime

from config import *
from utils import *
from servi_exceptions import *
import yaml
import getconfig


def rename_master_file(fname):
    # Renames the file  fname --> backup_fname__2014-09-04T17:32:44
    path = os.path.dirname(fname)
    newfname = 'backup_{0}_{1}'.format(
        os.path.basename(fname), datetime.utcnow().isoformat())

    shutil.move(fname, os.path.join(path, newfname))



def hash_of_file(fname):
    try:
        with open(fname, 'rb') as fp:
            content = fp.read()
            hashv = hashlib.sha1(content).hexdigest()
    except FileNotFoundError:
        hashv = MISSING_HASH
    return hashv



# Path functions
#


def templatepath_to_destpath(template_path):
    return pathfor(normalize_path(template_path, TEMPLATE), MASTER)


def pathfor(fname, source):
    return getconfig.pathfor(fname, source, TEMPLATE, MASTER,
                             TEMPLATE_DIR, MASTER_DIR)


def normalize_path(path, source):
    assert source in [TEMPLATE, MASTER]
    prefix = TEMPLATE_DIR if source is TEMPLATE else MASTER_DIR
    prefix += '/'
    if not os.path.commonprefix([prefix, path]) == prefix:
        raise Exception('Expected prefix ({0}) not found in path ({1})'
                        .format(prefix, path))
    return path.split(sep=prefix, maxsplit=1)[1]


def file_exists(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


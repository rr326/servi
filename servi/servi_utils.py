# servi_utils - utils that require servi/config.py

import hashlib

import servi.config as c
import servi.getconfig
from servi.servi_exceptions import *


def hash_of_file(fname):
    try:
        with open(fname, 'rb') as fp:
            content = fp.read()
            hashv = hashlib.sha1(content).hexdigest()
    except FileNotFoundError:
        hashv = c.MISSING_HASH
    return hashv

#
# Path functions
#


def templatepath_to_destpath(template_path):
    return pathfor(normalize_path(template_path, c.TEMPLATE), c.MASTER)


def pathfor(fname, source):
    return getconfig.pathfor(fname, source, c.TEMPLATE, c.MASTER,
                             c.MSTR_TMPL_DIR, c.MASTER_DIR)


def normalize_path(path, source):
    assert source in [c.TEMPLATE, c.MASTER]
    prefix = c.MSTR_TMPL_DIR if source is c.TEMPLATE else c.MASTER_DIR
    prefix += '/'
    if not os.path.commonprefix([prefix, path]) == prefix:
        raise Exception('Expected prefix ({0}) not found in path ({1})'
                        .format(prefix, path))
    return path.split(sep=prefix, maxsplit=1)[1]





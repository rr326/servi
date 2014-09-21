import os
import hashlib

import config as c
import getconfig


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
                             c.TEMPLATE_DIR, c.MASTER_DIR)


def normalize_path(path, source):
    assert source in [c.TEMPLATE, c.MASTER]
    prefix = c.TEMPLATE_DIR if source is c.TEMPLATE else c.MASTER_DIR
    prefix += '/'
    if not os.path.commonprefix([prefix, path]) == prefix:
        raise Exception('Expected prefix ({0}) not found in path ({1})'
                        .format(prefix, path))
    return path.split(sep=prefix, maxsplit=1)[1]


def file_exists(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def find_up(starting_dir, dirname):
    cur_dir = starting_dir

    while cur_dir != '/':
        if os.path.basename(cur_dir) == dirname:
            return cur_dir
        cur_dir = os.path.normpath(os.path.join(cur_dir, '..'))

    return None
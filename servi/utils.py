import hashlib
import os
import servi.config as c

import servi.globals as g


def qprint(*args, **kwargs):
    # quiet print - relies on 'import globals as g'
    if g.quiet:
        return
    print(*args, **kwargs)


def file_exists(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def hash_of_file(fname):
    try:
        with open(fname, 'rb') as fp:
            content = fp.read()
            hashv = hashlib.sha1(content).hexdigest()
    except FileNotFoundError:
        hashv = c.MISSING_HASH
    return hashv


def templatepath_to_destpath(template_path):
    return pathfor(normalize_path(template_path, c.TEMPLATE), c.MASTER)


def pathfor(fname, source):
    return c.pathfor(fname, source, c.TEMPLATE, c.MASTER, c.TMPL_DIR_SITE,
                     c.MASTER_DIR)


def normalize_path(path, source):
    assert source in [c.TEMPLATE, c.MASTER]
    prefix = c.TMPL_DIR_SITE if source is c.TEMPLATE else c.MASTER_DIR
    prefix += '/'

    assert os.path.commonprefix([prefix, path]) == prefix

    return path.split(sep=prefix, maxsplit=1)[1]
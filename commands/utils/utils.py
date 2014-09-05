import shutil
import json
import os
import hashlib
import re
from datetime import datetime

from config import *
from utils import *


def rename_master_file(fname):
    # Renames the file  fname --> backup_fname__2014-09-04T17:32:44
    path = os.path.dirname(fname)
    newfname = 'backup_{0}_{1}'.format(
        os.path.basename(fname), datetime.utcnow().isoformat())

    shutil.move(fname, os.path.join(path, newfname))


def copy_files(man, exclude_files):
    """
    man = manifest class for TEMPLATE (must be current)
    exclude_files = optional list of files to ignore

    Copies files from TEMPLATE_DIR to MASTER_DIR
    *Never* overrwrites - will always make a backup if file exists.
    """
    assert man.source == TEMPLATE
    
    for normalized_fname, template_hash in man.manifest["files"].items():
        if normalized_fname == VERSION_FILE:
            continue  # No need to copy version file (its in servi_data.json)

        template_fname = pathfor(normalized_fname, TEMPLATE)
        master_fname = pathfor(normalized_fname, MASTER)

        master_hash = hash_of_file(master_fname)

        # Exclude unchanged files
        if master_hash == template_hash:
            continue

        # Exclude ignored files
        if normalized_fname in exclude_files:
            continue

        # Always backup (never overwrite) master
        if file_exists(master_fname):
            rename_master_file(master_fname)
            existing = True
        else:
            existing = False

        # Copy template to master
        destdir = os.path.normpath(os.path.dirname(master_fname))
        if destdir:
            # noinspection PyArgumentList
            os.makedirs(destdir, exist_ok=True)
        shutil.copy2(template_fname, master_fname)
        if existing:
            qprint('Updated: {0}'.format(master_fname))
        else:
            qprint('Created: {0}'.format(master_fname))


def hash_of_file(fname):
    try:
        with open(fname, 'rb') as fp:
            content = fp.read()
            hashv = hashlib.sha1(content).hexdigest()
    except FileNotFoundError:
        hashv = MISSING_HASH
    return hashv


def ignored_files(files):
    """
    Looks in VERSION_FILE for a list of ignored files (regex)
    Returns the subset of input files that are matched.
    """
    with open(pathfor(VERSION_FILE, TEMPLATE)) as f:
        data = json.load(f)
    ignore_list = data["ignore"]
    ignore_re_string = '('+'|'.join(ignore_list)+')'
    ignore_re = re.compile(ignore_re_string)

    ignored = {file for file in files if ignore_re.search(file)}

    return ignored

#
# Path functions
#


def templatepath_to_destpath(template_path):
    return os.path.join(MASTER_DIR,  template_path[len(TEMPLATE_DIR)+1:])


def pathfor(fname, source):
    assert source in [TEMPLATE, MASTER]

    if source == TEMPLATE:
        path = os.path.normpath(os.path.join(TEMPLATE_DIR, fname))
    else:  # MASTER
        path = os.path.normpath(os.path.join(MASTER_DIR, fname))

    return path


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

import shutil
import json
import os
import hashlib
import re
from copy import deepcopy
from pprint import pformat
from datetime import datetime

from config import *
from servi_exceptions import *
from utils import *


def rename_master_file(fname):
    path = os.path.dirname(fname)
    newfname = 'backup_{0}_{1}'.format(
        os.path.basename(fname), datetime.utcnow().isoformat())

    shutil.move(fname, os.path.join(path, newfname))


def copy_files(manifest, exclude_files):
    for new_file, new_hash in manifest["files"].items():
        if new_file == pathfor(VERSION_FILE, TEMPLATE):
            continue  # No need to copy version file (its in servi_data.json)

        master = templatepath_to_destpath(new_file)
        try:
            master_hash = hash_of_file(master)
        except IOError:
            master_hash = None

        if master_hash == new_hash:
            continue

        if exclude_files and os.path.isfile(master) and \
                normalize_path(new_file, TEMPLATE):
            continue

        if os.path.isfile(master):
            rename_master_file(master)
            existing = True
        else:
            existing = False

        destdir = os.path.normpath(os.path.dirname(master))
        if os.path.dirname(destdir):
            # noinspection PyArgumentList
            os.makedirs(destdir, exist_ok=True)
        shutil.copyfile(new_file, master)
        if existing:
            qprint('Updated: {0}'.format(master))
        else:
            qprint('Created: {0}'.format(master))




def hash_of_file(fname):
    with open(fname, 'rb') as fp:
        content = fp.read()
        hashv = hashlib.sha1(content).hexdigest()
    return hashv


def remove_ignored_files(files):
    with open(pathfor(VERSION_FILE, TEMPLATE)) as f:
        data = json.load(f)
    ignore_list =  data["ignore"]
    ignore_re_string = '('+'|'.join(ignore_list)+')'
    ignore_re = re.compile(ignore_re_string)

    new_files=files.copy()
    for file in files:
        if ignore_re.search(file):
            new_files.remove(file)

    print("DEBUG: Ignored_files: {0}".format(files-new_files))
    return new_files
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

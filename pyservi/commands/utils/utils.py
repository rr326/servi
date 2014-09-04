import shutil
import json
import os
import hashlib
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


def copy_files(manifest):
    for new_file, new_hash in manifest["files"].items():
        master = templatepath_to_destpath(new_file)
        try:
            master_hash = hash_of_file(master)
        except IOError:
            master_hash = None

        if master_hash == new_hash:
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


def error_if_changed(force, changed_files, existing_version,
                     new_version):
    if not force and changed_files:
        raise ForceError(
            'The following files from the template were changed'
            ' unexpectedly: {0}'.format(changed_files))

    if not force and existing_version > new_version:
        raise ForceError('Existing template version ({0}) '
                         '> new version ({1})'
                         .format(existing_version, new_version))


def find_deleted_files():
    """
    Figure out what files the user has intentionally deleted from the
    template structure. (eg: apache_config/sites-available/THISSITE.conf)
    deleted =
        * old-deleted: anything in the master manifest's "deleted" list
        * newly-deleted: anything the master manifest says should be there and
           isn't
    """
    servi_data_file = templatepath_to_destpath(VERSION_FILE)
    try:
        with open(servi_data_file, 'r') as fp:
            existing_manifest = json.load(fp)
    except FileNotFoundError:
        raise ServiError('The servi data file ({0}) was not found.\n'
                         'servi needs this to update properly.'
                         .format(servi_data_file))

    print('existing manifest: \n{0}'.format(pformat(existing_manifest)))
    exit()


def hash_of_file(fname):
    with open(fname, 'rb') as fp:
        content = fp.read()
        hashv = hashlib.sha1(content).hexdigest()
    return hashv


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



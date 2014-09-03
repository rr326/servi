from config import *
import globals as g
from utils import *
import shutil
import json
import os
import hashlib
from pprint import pprint, pformat
from datetime import datetime

def get_template_version(file):
    with open(file) as f:
        data = json.load(f)
    return data["template_version"]


def hash_of_file(fname):
    with open(fname, 'rb') as fp:
        content = fp.read()
        hashv = hashlib.sha1(content).hexdigest()
    return hashv


def create_manifest():
    # Return a dict of all template files and their SHA1 hash
    #  (and the template version - eg: 1.0.0)
    manifest = {
        "files": {},
        "template_version": get_template_version(VERSION_FILE)
    }

    for (dirpath, dirnames, filenames) in os.walk(TEMPLATE_DIR):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            manifest["files"][fullpath] = hash_of_file(fullpath)
    return manifest


def templatepath_to_destpath(template_path):
    return os.path.join(MASTER_DIR,  template_path[len(TEMPLATE_DIR)+1:])


def compare_digests(manifest):
    # Returns a list of files that are in the template directory but have
    # been changed in the master directory
    warn = []
    for file, sha1 in manifest["files"].items():
        path = templatepath_to_destpath(file)
        if os.path.isfile(path) and os.access(path, os.R_OK):
            if hash_of_file(path) != sha1:
                warn.append(path)
    return warn


def compare_template_versions(manifest):
    try:
        existing_version = get_template_version(
            templatepath_to_destpath(VERSION_FILE))
    except FileNotFoundError:
        existing_version = ''
    return existing_version, manifest["template_version"]


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

        destdir = os.path.abspath(os.path.dirname(master))
        if os.path.dirname(destdir):
            os.makedirs(destdir, exist_ok=True)
        shutil.copyfile(new_file, master)
        if existing:
            qprint('Updated: {0}'.format(master))
        else:
            qprint('Created: {0}'.format(master))
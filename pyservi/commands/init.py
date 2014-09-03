from config import *
from Command import Command
from servi_exceptions import ForceError

import shutil
import json
import os
import hashlib
from pprint import pprint, pformat
from datetime import datetime


def qprint(*args, **kwargs):
    # quiet print - relies on GLOBAL quiet
    if quiet:
        print('qprint')
        return
    print(*args, **kwargs)


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


def check_errors(force, changed_files, existing_version, new_version):
    if not force and changed_files:
        raise ForceError('The following files from the template were changed'
                         ' unexpectedly: {0}'.format(changed_files))

    if not force and existing_version > new_version:
        raise ForceError('Existing template version ({0}) '
                         '> new version ({1})'.format(existing_version,
                         new_version))


def rename_master_file(fname):
    path = os.path.dirname(fname)
    newfname = 'backup_{0}_{1}'.format(os.path.basename(fname),
        datetime.utcnow().isoformat())

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
            qprint('Replaced file:    {0}'.format(master))
        else:
            qprint('Created new file: {0}'.format(master))
       


class InitCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser('init', help='Init project')
        parser_init.add_argument('-f', '--force', action='store_true')
        parser_init.add_argument('-q', '--quiet', action='store_true')
        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        global quiet
        quiet = args.quiet
        print('init.run() called with args: {0}'.format(args))

        manifest = create_manifest()
        changed_files = compare_digests(manifest)
        existing_version, new_version = compare_template_versions(manifest)

        check_errors(
            force=args.force, changed_files=changed_files,
            existing_version=existing_version, new_version=new_version)

        copy_files(manifest)


print('**init.py**')
command=InitCommand()

## TODO - How to deal with files that were deleted in MASTER_DIR (eg: THIS_SITE.conf)
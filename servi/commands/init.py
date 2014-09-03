from config import *
import json
import os
import hashlib
#import ..Command
from pprint import pformat, pprint



def get_template_version(file):
    with open(file) as f:
        data = json.load(f)
    return data["template_version"]


def create_manifest():
    # Return a dict of all template files and their SHA1 hash
    #  (and the template version - eg: 1.0.0)
    manifest = { "files" : {}}
    manifest["template_version"] = get_template_version(VERSION_FILE)

    for (dirpath, dirnames, filenames) in os.walk(TEMPLATE_DIR):
        for file in filenames:
            fullpath=os.path.join(dirpath, file)
            with open(fullpath, 'rb') as fp:
                content = fp.read()
                manifest["files"][fullpath] = hashlib.sha1(content).hexdigest()
    return manifest


def templatepath_to_destpath(template_path):
    return os.path.join(DEST_DIR,  template_path[len(TEMPLATE_DIR)+1:])


def compare_digests(manifest):
    # Returns a list of files that are in the template directory but have
    # been changed in the master directory
    warn = []
    for file, sha1 in manifest["files"].items():
        path = templatepath_to_destpath(file)
        if os.path.isfile(path) and os.access(path, os.R_OK):
            with open(path, 'rb') as fp:
                content = fp.read()
                if hashlib.sha1(content).hexdigest() != sha1:
                    warn.append(path)
    return warn


def compare_template_versions(manifest):
    existing_version = get_template_version(
        templatepath_to_destpath(VERSION_FILE))
    return existing_version, manifest["template_version"]


def do_init(manifest, force, changed_files, existing_version, new_version):
    if not force and changed_files:
        for file in changed_files:
            print("Error: file changed in master: {0}".format(file))
        raise Exception('Files Changed - Aborting (use "--force" to ignore)')

    if not force and existing_version > new_version:
        raise Exception('existing template version > new version: '
              ' existing: {0} > new: {1}\nAborting (use "--force" to ignore) '.
              format(existing_version, new_version))


def run(args):
    print('servi_init: args.force: {0}'.format(args.force))

    manifest = create_manifest()
    changed_files = compare_digests(manifest)
    existing_version, new_version = compare_template_versions(manifest)

    do_init(manifest, force=args.force, changed_files=changed_files,
        existing_version=existing_version, new_version=new_version)


if __name__ == "__main__":
    pass

print('**init.py**')
from config import *
import json
import os
import hashlib
from pprint import pformat, pprint


def get_template_version():
    with open(VERSION_FILE) as f:
        data = json.load(f)
    return data["template_version"]


def create_manifest():
    # Return a dict of all template files and their SHA1 hash
    #  (and the template version - eg: 1.0.0)
    manifest = { "files" : {}}
    manifest["template_version"] = get_template_version()

    for (dirpath, dirnames, filenames) in os.walk(TEMPLATE_DIR):
        for file in filenames:
            fullpath=os.path.join(dirpath, file)
            with open(fullpath, 'rb') as fp:
                content = fp.read()
                manifest["files"][fullpath] = hashlib.sha1(content).hexdigest()
    return manifest


def compare_digests(manifest):
    for file, sha1 in manifest["files"].items():
        path = os.path.join(DEST_DIR,  file[len(TEMPLATE_DIR)+1:])
        if not (os.path.isfile(path) and os.access(path, os.R_OK)):
            print('Path doesnt exist: ', path)
        else:
            with open(path, 'rb') as fp:
                content = fp.read()
                if hashlib.sha1(content).hexdigest() != sha1:
                    print('File changed: ', path)
                else:
                    pass
                    #print('All good: ', path)




def run():
    print('cwd: ', os.getcwd())
    manifest = create_manifest()
    compare_digests(manifest)

if __name__ == "__main__":
    run()
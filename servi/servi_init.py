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
    manifest={ "files" : {}}
    manifest["template_version"] = get_template_version()

    for (dirpath, dirnames, filenames) in os.walk(TEMPLATE_DIR):
        for file in filenames:
            fullpath=os.path.join(dirpath, file)
            with open(fullpath, 'rb') as fp:
                content = fp.read()
                manifest["files"][fullpath] = hashlib.sha224(content).hexdigest()
    return manifest


def run():
    manifest = create_manifest()

if __name__ == "__main__":
    run()
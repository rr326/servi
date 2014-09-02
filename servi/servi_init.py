import json
from config import *

def get_template_version():
    with open(VERSION_FILE) as f:
        data=json.load(f)
    return data["template_version"]

def run():
    print("In servi_init.py --> run()")
    template_version = get_template_version()
    print("template_version: {0}".format(template_version))


if __name__ == "__main__":
    run()
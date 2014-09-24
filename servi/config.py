import os
import os.path
import yaml
from servi.servi_exceptions import MasterNotFound

'''
Global configuration for servi files
Use as import config as c
Note - this will also read in additional variables (and overrides) from
SERVI_CONFIG_YML

Proper dir structure
servi installation -
  eg: pyvenv/py3.4/lib/python3.4/site-packages/servi-0.1-py3.4.egg/servi

Project
  ...\masterdir
          \servi
              \servi   # Kinda ugly that it has the smae name, but helpful
                         for argparse
              \sevi_templates
'''

SERVI_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
TMPL_DIR_SITE = \
    os.path.normpath(os.path.join(SERVI_DIR, 'servi_templates'))

# These must be initialized and then set here as c.MASTER_DIR =xxx
MASTER_DIR = None

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"
SERVI_CONFIG_YML = "Servifile.yml"

TEMPLATE = 'template'
MASTER = 'master'
MISSING_HASH = 'FILE NOT FOUND'

# The following must be set in Servifile.yml
SERVI_IGNORE_FILES = []
DIFFTOOL = 'git diff'


def set_master_dir(set_dir_to):
    """
    sets c.MASTER_DIR
        by finding the first ancestor(default)
        to set_dir_to (if supplied - only for servi init)
    """
    global MASTER_DIR

    MASTER_DIR = set_dir_to
    # TODO - remove this function


def load_user_config():
    user_config = getconfig(
        SERVI_CONFIG_YML, TEMPLATE, MASTER, TMPL_DIR_SITE, MASTER_DIR)

    for key, value in user_config.items():
        globals()[key] = value


def find_master_dir(start_dir, fail_ok=False):
    """
    Returns the master dir with the following signature at or above start_dir:
    MASTER_DIR
        \servi
            \servi_templates
    raises MasterNotFound if not found
    (if failok, and not found, returns None)
    """
    servi_dir = find_ancestor_with(start_dir, 'servi')
    if (not servi_dir or
            not os.path.exists(
                os.path.join(servi_dir, 'servi/servi_templates'))):

        if fail_ok:
            return None
        else:
            raise MasterNotFound(os.getcwd())
    return servi_dir

def find_ancestor_with(starting_dir, dirname):
    """
    returns first ancestor of starting_dir that contains dirname
    (returns abspath())
    returns None if not found
    """
    cur_dir = os.path.abspath(starting_dir)

    while cur_dir != '/':
        if os.path.exists(os.path.join(cur_dir, dirname)):
            return cur_dir
        cur_dir = os.path.abspath(os.path.normpath(os.path.join(cur_dir, '..')))

    return None


def servi_file_exists_in(path):
    return os.path.exists(os.path.join(path, SERVI_CONFIG_YML))

"""
This is an ugly, parameterized version of pathfor, and a getconfig() which
relies on it. I need it since the other pathfor uses config parameters
(which this bootstraps).

Only use this in the config module.
After that, use commands.utils.utils.pathfor()
"""



def pathfor(fname, source, template, master, template_dir, master_dir):
    assert source in [template, master]

    if source == template:
        path = os.path.normpath(os.path.join(template_dir, fname))
    else:  # MASTER
        path = os.path.normpath(os.path.join(master_dir, fname))

    return path


def getconfig(fname, template, master, template_dir, master_dir):
    # if master_dir:
    #     try:
    #         with open(pathfor(fname, master, template, master,
    #                   template_dir, master_dir)) as f:
    #             data = yaml.load(f)
    #             return data
    #     except FileNotFoundError:
    #         # ok - retry with template
    #         pass
    #
    # # master_dir is None or FileNotFoundError
    # with open(pathfor(fname, template, template, master,
    #         template_dir, master_dir)) as f:
    #     data = yaml.load(f)
    #
    # return data
    # TODO - clean up getconfig
    with open(pathfor(fname, master, template, master, template_dir,
              master_dir)) as f:
                data = yaml.load(f)
                return data
import os
import os.path
import yaml
from servi.exceptions import MasterNotFound, ServiError
import logging
from jinja2 import Environment, DictLoader

'''
Global configuration for servi files
Use as import config as c
Note - this will also read in additional variables (and overrides) from
SERVIFILE

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
BOX_DIR = os.path.abspath(os.path.join(SERVI_DIR, 'servi_boxes'))

# These must be initialized and then set here as c.MASTER_DIR =xxx
MASTER_DIR = None

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"
SERVIFILE = "Servifile.yml"

TEMPLATE = 'template'
MASTER = 'master'
MISSING_HASH = 'FILE NOT FOUND'

# The following must be set in Servifile.yml
SERVI_IGNORE_FILES = []
DIFFTOOL = 'git diff'

LOG_LEVEL = logging.DEBUG


#############################################################################
#############################################################################
#############################################################################
LOOKUP_FAILED_MESSAGE = 'Environment variable not found'


def lookup(ltype, arg1):
    if type(ltype) is not str or ltype.strip().lower() != 'env':
        raise ServiError('Found "lookup" function that servi does not'
                         'understand ({0}). Currently servi only processes'
                         'lookup("env", variable") - which mimics a portion'
                         'of ansibles lookup function.')
    retval = os.environ.get(arg1)
    if retval is None:
        retval = LOOKUP_FAILED_MESSAGE
    return retval


def setup_jinja(env=None, template_text=None):
    if env is None:
        env = Environment(loader=DictLoader({SERVIFILE: template_text}))
    env.globals['lookup'] = lookup
    return env


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
    """
    Reads and processes Servifile.yml, adding all variables to this modules
    globals()

    Step 1: Read Servifile
    Step 2: Render the file as a Jinja2 template
                (with custom function: lookup('env', envvar) )
    Step 3: Load as a yaml doc
    Step 4: Add to this module's globals()
    """
    user_config = getconfig(
        SERVIFILE, TEMPLATE, MASTER, TMPL_DIR_SITE, MASTER_DIR)

    for key, value in user_config.items():
        globals()[key] = value

    return True


def find_master_dir(start_dir, fail_ok=False):
    """
    finds Servifile.yml at or above start_dir
    returns MasterNotFound or None (if fail_ok)
    """
    master_dir = find_ancestor_servifile(start_dir)
    if not master_dir:
        if not fail_ok:
            raise MasterNotFound()
        else:
            return None
    else:
        return os.path.abspath(master_dir)


def find_ancestor_servifile(starting_dir):
    return find_ancestor_with(starting_dir, SERVIFILE)


def find_ancestor_with(starting_dir, target):
    """
    returns first ancestor of starting_dir that contains target (dir or file)
    (returns abspath())
    returns None if not found
    """
    cur_dir = os.path.abspath(starting_dir)

    while cur_dir != '/':
        if os.path.exists(os.path.join(cur_dir, target)):
            return cur_dir
        cur_dir = os.path.abspath(
            os.path.normpath(os.path.join(cur_dir, '..')))

    return None


def servi_file_exists_in(path):
    return os.path.exists(os.path.join(path, SERVIFILE))

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
    with open(pathfor(fname, master, template, master, template_dir,
              master_dir)) as f:
                servi_raw = f.read()

    return process_config(servi_raw)


def process_config(raw_text):
    env = setup_jinja(env=None, template_text=raw_text)
    tmpl = env.get_template(SERVIFILE)
    rendered = tmpl.render()
    data = yaml.load(rendered)
    return data
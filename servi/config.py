import os
from getconfig import getconfig
from utils import find_master_dir


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

MASTER_DIR = find_master_dir()
MSTR_TMPL_DIR = \
    os.path.normpath(os.path.join(MASTER_DIR, 'servi/servi_templates'))


MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"
SERVI_CONFIG_YML = "servi_config.yml"

TEMPLATE = 'template'
MASTER = 'master'
MISSING_HASH = 'FILE NOT FOUND'

# The following must be set in servi_config.yml
SERVI_IGNORE_FILES, DIFFTOOL = None, None

# Now read in config from SERVI_CONFIG_YML
c = getconfig(SERVI_CONFIG_YML, TEMPLATE, MASTER, MSTR_TMPL_DIR, MASTER_DIR)
g = globals()
for key, value in c.items():
    g[key] = value


#
# Mock overrides
#
# For testing I may need to set an environment variable to ovverride a config
# parameter (eg: MSTR_TMPL_DIR = 'tmp/mock/templates'
# (I can't just use pytest monkeypatch because A) I do a subprocess() call
# and B) do 'import config as c')
_overrides = ['MSTR_TMPL_DIR']
for _override in _overrides:
    if _override in os.environ:
        print('config: {0} override set in environment variable: {1} '.
              format(_override, os.environ[_override]))
        globals()[_override] = os.environ[_override]

import os



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
MSTR_TMPL_DIR = None

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"
SERVI_CONFIG_YML = "servi_config.yml"

TEMPLATE = 'template'
MASTER = 'master'
MISSING_HASH = 'FILE NOT FOUND'

# The following must be set in servi_config.yml
SERVI_IGNORE_FILES, DIFFTOOL = None, None

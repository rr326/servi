import os
from getconfig import getconfig

#
# Global configuration for servi files
# Use as import config as c
# Note - this will also read in additional variables (and overrides) from
# SERVI_CONFIG_YML
#

SERVI_DIR = os.path.normpath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(SERVI_DIR, 'templates'))
MASTER_DIR = os.path.normpath(os.path.join(SERVI_DIR, '..'))

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"
SERVI_CONFIG_YML = "servi_config.yml"

TEMPLATE = 'template'
MASTER = 'master'
MISSING_HASH = 'FILE NOT FOUND'

# The following must be set in servi_config.yml
SERVI_IGNORE_FILES, DIFFTOOL = None, None

# Now read in config from SERVI_CONFIG_YML
c = getconfig(SERVI_CONFIG_YML, TEMPLATE, MASTER, TEMPLATE_DIR, MASTER_DIR)
g = globals()
for key, value in c.items():
    g[key] = value


#
# Mock overrides
#
# For testing I may need to set an environment variable to ovverride a config
# parameter (eg: TEMPLATE_DIR = 'tmp/mock/templates'
# (I can't just use pytest monkeypatch because A) I do a subprocess() call
# and B) do 'import config as c')
_overrides = ['TEMPLATE_DIR']
for _override in _overrides:
    if _override in os.environ:
        print('config: {0} override set in environment variable: {1} '.
              format(_override, os.environ[_override]))
        globals()[_override] = os.environ[_override]

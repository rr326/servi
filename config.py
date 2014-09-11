import os
from getconfig import getconfig

#
# Global configuration for servi files
# Use as from config import *
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
config = getconfig(SERVI_CONFIG_YML, TEMPLATE, MASTER,
                   TEMPLATE_DIR, MASTER_DIR)
g = globals()
for key, value in config.items():
    g[key] = value


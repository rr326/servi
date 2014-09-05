import os.path

TEMPLATE = 'template'
MASTER = 'master'

SERVI_DIR = os.path.normpath(os.path.dirname(__file__))

TEMPLATE_DIR = os.path.normpath(os.path.join(SERVI_DIR, 'templates'))
MASTER_DIR = os.path.normpath(os.path.join(SERVI_DIR, '..'))

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"

MISSING_HASH = 'FILE NOT FOUND'

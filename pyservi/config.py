import os.path

TEMPLATE = 'template'
MASTER = 'master'

PYSERVI_DIR = os.path.normpath(os.path.dirname(__file__))
ROOT_DIR = os.path.normpath(os.path.join(PYSERVI_DIR, '..'))

TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
MASTER_DIR = os.path.normpath(os.path.join(ROOT_DIR, '..'))

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"

# TODO - Move to relative paths? (rooted at boilerplate dir?)
import os.path

TEMPLATE = 'template'
MASTER = 'master'

print('__file__: {0}'.format(__file__))
print('abspath: {0}'.format(os.path.abspath(os.path.dirname(__file__))))

PYSERVI_DIR = os.path.normpath(os.path.dirname(__file__))
ROOT_DIR = os.path.normpath(os.path.join(PYSERVI_DIR, '..'))

TEMPLATE_DIR = os.path.normpath(os.path.join(ROOT_DIR, 'templates'))
MASTER_DIR = os.path.normpath(os.path.join(ROOT_DIR, '..'))

MANIFEST_FILE = "servi_data.json"
VERSION_FILE = "TEMPLATE_VERSION.json"

MISSING_HASH = 'FILE NOT FOUND'
# TODO - Move to relative paths? (rooted at boilerplate dir?)
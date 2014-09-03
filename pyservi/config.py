import os.path

PYSERVI_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(PYSERVI_DIR, '..'))

TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
VERSION_FILE = os.path.join(TEMPLATE_DIR, "template_version.json")
MASTER_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..'))

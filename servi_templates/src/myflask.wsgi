import site
site.addsitedir('/usr/share/penv/py3/lib/python3.4/site-packages')

import sys
sys.path.insert(0, '/var/www/mysite')

from myflask import app as application
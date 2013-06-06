import os
import sys	
sys.path.append('/home/mlm/public_html/mlmsite.com/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DiamondMLM.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

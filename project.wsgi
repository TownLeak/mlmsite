import os
import sys	
sys.path.append('~/public_html/mlmsite.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DiamondMLM.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

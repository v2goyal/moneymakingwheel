import os
import sys
sys.path = ['/var/www/firstWebsite'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'firstWebsite.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

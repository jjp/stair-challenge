import logging, os, sys

# Google App Engine imports
from google.appengine.ext.webapp import util

# Force Django to reload all settings
from django.conf import settings
settings._target = None

# Must set this env var befor importing any of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'stairchallenge.settings'
sys.path.append(os.path.dirname(sys.argv[0]))

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

def log_exception( *args, **kwds ):
    logging.exception('Exception in request: ' )

# log errors
django.dispatch.dispatcher.connect(
    log_exception, django.core.signals.got_request_exception )

# unregister the rollback event handler
django.dispatch.dispatcher.disconnect(
    django.db._rollback_on_exception,
    django.core.signals.got_request_exception )

def main():
    # create a django application for wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

    # run the WSGI CGI handler for that application
    util.run_wsgi_app( application )

if __name__ == '__main__':
    main()

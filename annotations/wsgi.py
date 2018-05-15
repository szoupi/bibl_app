"""
WSGI config for annotations project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/

edit also
/etc/apache2/sites-available/000-default.conf
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "annotations.settings")

application = get_wsgi_application()

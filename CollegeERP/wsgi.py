"""
WSGI config for CollegeERP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')


from django.core.wsgi import get_wsgi_application
from whitenose import WhiteNose


application = get_wsgi_application()
# application = DjangoWhiteNoise(application)

application = CollegeERP()
application = WhiteNoise(application, root="/AttendenceMgtSys/staticfiles")

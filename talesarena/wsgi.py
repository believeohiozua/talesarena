"""
WSGI config for talesarena project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talesarena.settings')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'talesarena.settings'
# application = get_wsgi_application()
application = WhiteNoise(get_wsgi_application())
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
application.add_files(os.path.join(BASE_DIR, 'staticfiles'))
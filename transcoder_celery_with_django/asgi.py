# import os
# import django
# from channels.routing import get_default_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcoder_celery_with_django.settings')
# django.setup()
#
# application = get_default_application()
#
# # application = ProtocolTypeRouter({
# #     "http": AsgiHandler(),
# #
# #     "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
# #     # "websocket": AllowedHostsOriginValidator(
# #     #     AuthMiddlewareStack(URLRouter(ws_urlpatterns))
# #     # ),
# # })

"""
ASGI config for legal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.http import AsgiHandler
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcoder_celery_with_django.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from .routing import ws_urlpatterns


application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})


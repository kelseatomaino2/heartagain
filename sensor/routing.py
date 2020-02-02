from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import sensorWorker.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
       # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            sensorWorker.routing.websocket_urlpatterns
        )
    ),
})

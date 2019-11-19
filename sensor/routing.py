from channels.auth import AuthMiddlewareStack
from sensor.consumers import EventConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
import heartagain.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
     'websocket': AuthMiddlewareStack(
        URLRouter(
            heartagain.routing.websocket_urlpatterns
        )
    ),
})

channel_routing = {
    'websocket.connect': EventConsumer.ws_connect,
    'websocket.receive': EventConsumer.ws_receive,
    'websocket.disconnect': EventConsumer.ws_disconnect,
}

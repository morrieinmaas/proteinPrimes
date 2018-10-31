from channels import route
from primeQure import consumers

channel_routing = [
    #  Wire up websocket channels to our consumers:
    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_receive),
]
#  from channels.routing import ProtocolTypeRouter, URLRouter
#  from channels.auth import AuthMiddlewareStack
#  import primeQure.routing
#
#  application = ProtocolTypeRouter({
    #  'websocket': AuthMiddlewareStack(
        #  URLRouter(
            #  primeQure.routing.websocket_urlpatterns
        #  )
    #  ),
#  })

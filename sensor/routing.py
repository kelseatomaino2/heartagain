from sensor.consumers import ws_message, ws_connect, ws_disconnect

channel_routing = {
    'websocket.connect': ws_connect,
    'websocket.receive': ws_message,
    'websocket.disconnect': ws_disconnect,
}
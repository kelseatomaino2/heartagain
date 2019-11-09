from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
import json

class EventConsumer(WebsocketConsumer):

    def ws_connect(self, text_data):
        path = message['path']
        self.group_name = 'sensor'
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if path == '/sensor/':
            print("Adding new user to sensor group")
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name)

            async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'sensor_reading',
                'message': message
            }
        )

        self.accept()

    def ws_disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def ws_receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'sensor_reading',
                'message': message
            }
        )
       
    
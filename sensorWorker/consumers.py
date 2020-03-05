# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class EventConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_group_name = 'sensor'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

   
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(ecg_value)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_json
        )

    # Receive message from room group
    def sensor_reading(self, event):
        ecg_value = event['ecg_value']
        flow_value = event['flow_value']
        bpm_value = event['bpm_value']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'ecg_value': ecg_value,
            'flow_value': flow_value,
            'bpm_value': bpm_value,
        }))
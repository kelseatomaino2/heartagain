from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
import json

class EventConsumer(WebsocketConsumer):

    def ws_connect(self):
        self.accept()

    def ws_disconnect(self, close_code):
        print("disconnect")
        pass

    def ws_receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
       
       
            
        

    # def ws_connect(message):
    #     print("Someone connected.")
    #     path = message['path']                                                      # i.e. /sensor/

    #     if path == b'/sensor/':
    #         print("Adding new user to sensor group")
    #         Group("sensor").add(message.reply_channel)                             # Adds user to group for broadcast
    #         message.reply_channel.send({                                            # Reply to individual directly
    #            "text": "You're connected to sensor group :) ",
    #         })
    #     else:
    #         print("Strange connector!!")

    # def ws_message(message):
    #     # ASGI WebSocket packet-received and send-packet message types
    #     # both have a "text" key for their textual data.
    #     print("Received!!" + message['text'])

    # def ws_disconnect(message):
    #     print("Someone left us...")
    #     Group("sensor").discard(message.reply_channel)

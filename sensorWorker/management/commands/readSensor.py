from django.core.management import BaseCommand
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer


# This class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help="Simulates reading sensor and sending over Channel."

    # A command must define handle()
    def handle(self, *args, **options):
        self.channel_layer = get_channel_layer()
        self.group_name = 'sensor'
        x = 0
        while True:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type' : 'sensor_reading',
                    'message': 'sensor_reading...' + str(x),
                }
            )
            time.sleep(1)
            x+=1
            self.stdout.write("Sensor reading..." + str(x))

from django.core.management import BaseCommand
from gpiozero import MCP3008
import time, sys
import RPI.GPIO as GPIO
import numpy as np
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
        
        flow_sensor = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)
              
        global count
        count = 0
        
        def countPulse(channel):
           global count
           if start_counter == 1:
              count = count+1
        #      print count
        #      flow = count / (60 * 7.5)
        #      print(flow)
        
        GPIO.add_event_detect(flow_sensor, GPIO.FALLING, callback=countPulse)
        
        while True:
            try:
                start_counter = 1
                time.sleep(1)
                start_counter = 0
                flow = (count * 60 * 2.25 / 1000)
                #print ("The flow is: %.3f Liter/min" % flow)
                count = 0
                time.sleep(5)
            except KeyboardInterrupt:
                #print ('\ncaught keyboard interrupt!, bye')
                GPIO.cleanup()
                sys.exit()

        while True:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type' : 'sensor_reading',
                    'message': 'sensor_reading...' + str(flow),
                }
            )
            time.sleep(1)
            x+=1
            self.stdout.write("Sensor reading..." + str(flow))

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
        
        #Setup pins - ADC
        flow_sensor = 23
        ECG_output = MCP3008(channel=0, device=0)
        #flow_out = MCP3008(channel=1, device=0) #when using the transonic, test sensor is digital
        #flow_in = MCP3008(channel=2, device=0) #when using the transonic, test sensor is digital
        pressure_oxy = MCP3008(channel=3, device=0)
        pressure_deoxy = MCP3008(channel=4, device=0)
        pressure_negative = MCP3008(channel=5, device=0)
        temperature = MCP3008(channel=6, device=0)
        
        #Setup up pins - digital
        flow_sensor = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(22,GPIO.IN) #LOD+
        GPIO.setup(27,GPIO.IN) #LOD-
        
        #Set up ECG variables        
        self.BPM = 0
        self.beat_old = 0
        self.beats = np.zeros(500)  # Used to calculate average BPM, creates a 1D array of size 500
        self.beatIndex = 0
        self.threshold = 620.0  #Threshold at which BPM calculation occurs
        self.belowThreshold = True
        
        #Set up flow variables
        # global count
        self.count = 0
        
        GPIO.add_event_detect(flow_sensor, GPIO.FALLING, callback=countPulse)
        
        pressure = 40
        temperature = 37

        self.room_group_name = 'sensor'
        x = 0
        while True:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type' : 'sensor_reading',
                    'ecg_value': ECG,
                    'bpm': BPM,
                    'flow_value': flow,
                    'pressure_value': pressure,
                    'temperature_value': temperature,
                }
            )
            time.sleep(1)
            
            # Sensor update section
            
            # ECG leads on check and update
            if (GPIO.input(22) == 1 and GPIO.input(27) ==1):
                print("Electrodes not connected")
            else:
                ECG = ECG_output.value
                print(ECG)
                time.sleep(100)
                
            # BPM calculation check
            if (ECG_output.value > threshold and belowThreshold == true):
                BPM = calculateBPM()
                belowThreshold = false
            
            elif(ECG_output.value < threshold):
                belowThreshold = true 
                
            # Other sensor updates
            flow = self.count / (60 * 7.5)
            #pressure =  pressure_oxy.value
            #temperature = temperature.value
            
            self.stdout.write("ECG reading..." + str(self.ECG))
            self.stdout.write("BPM reading..." + str(self.BPM))
            self.stdout.write("Flow reading..." + str(flow))
            #self.stdout.write("Flow reading..." + str(pressure))
            #self.stdout.write("Flow reading..." + str(temperature))
                  
            
    def countPulse(channel):
        self.count = self.count + 1
        flow = self.count / (60 * 7.5)
        return flow
        
    def calculateBPM(self):
        beat_new = int(round(time.time() * 1000))   #get current time
        diff = beat_new - self.beat_old
        currentBPM = 60000 / diff;    #convert to BPM
        self.beats[self.beatIndex] = currentBPM #store for avg
        total = sum(self.beats)
        # for i in range (0,500):
            # total = total + self.beats(1,i)
        BPM = total / 500
        self.beat_old = beat_new;
        beatIndex = (beatIndex + 1) % 500
        return BPM



        
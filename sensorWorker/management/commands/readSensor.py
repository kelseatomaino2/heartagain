from django.core.management import BaseCommand
from gpiozero import MCP3008
import time, sys
#import RPi.GPIO as GPIO
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
from sensorWorker.models import EcgData
from sensorWorker.models import FlowData
from sensorWorker.models import Session
import datetime


# This class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help="Simulates reading sensor and sending over Channel."


    # A command must define handle()
    def handle(self, *args, **options):
        self.channel_layer = get_channel_layer()

        # This method is a background task used to read sensor outputs, send values to the UI for display
        # Values are stored in the database 
        
        #Setup pins - AD 
        # These pins are used with the ADC for analog sensors
        #self.ECG_output = MCP3008(channel=0, device=0)
        #self.flow_out = MCP3008(channel=1, device=0) #when using the transonic, test sensor is digital
        #self.flow_in = MCP3008(channel=2, device=0) #when using the transonic, test sensor is digital
        #self.pressure_oxy = MCP3008(channel=3, device=0)
        #self.pressure_deoxy = MCP3008(channel=4, device=0)
        #self.pressure_negative = MCP3008(channel=5, device=0)
        #self.temperature = MCP3008(channel=6, device=0)
        
        #Setup up pins - digital
        flow_sensor = 23
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        #GPIO.setup(22,GPIO.IN) # LOD+
        #GPIO.setup(27,GPIO.IN) # LOD-
        
        #Set up ECG variables        
        self.BPM = 0
        self.ECG = 0
        self.flow = 0
        self.beat_old = 0
        self.beats = [0] * 4 
        self.beatIndex = 0
        self.threshold = 0.9  #Threshold at which BPM calculation occurs
        self.belowThreshold = True
        
        self.count = 0
        # This is used to simulate ECG data. These are fake values in database
        self.aeg_values = EcgData.objects.all().filter(user_id='testid2')
        self.total_aeg_values = self.aeg_values.count()
        self.user_id = Session.objects.latest('start_date').user_id


        def count_pulse(channel):
            self.count = self.count + 1
            return self.count
        
        #GPIO.add_event_detect(flow_sensor, GPIO.FALLING, callback=count_pulse)

        self.room_group_name = 'sensor'
        x = 0
        i = 0
        flow_alert = False
        self.ecg_values = []
        self.flow_values = []
        # This is an infinite loop that needs to be fixed. It is displayed via start and stop in the UI.
        while True: 
            # Following if statement needs to be replaced by self.take_ecg_reading()
            if(i==self.total_aeg_values):
                i = 0
                self.ECG = float(self.aeg_values[i].ecg_value)
            else:
                self.ECG = float(self.aeg_values[i].ecg_value)
                i = i+1    
            # BPM calculation check
            if (self.ECG > self.threshold and self.belowThreshold == True):
                self.BPM = self.calculate_BPM()
                belowThreshold = False
            
            elif(self.ECG < self.threshold):
                belowThreshold = True 
                
            # Other sensor updates
            if(x==2):
                self.flow = self.count / (7.5)
                self.count = 0
                x = 0
            else:
                x = x+1
            #pressure =  pressure_oxy.value
            #temperature = temperature.value

            if(self.flow==0):
                flow_alert = True
            else:
                flow_alert = False
            
            #TODO: Add values to arrays for other sensors and insert statements
            ecg_dict = {'date_time': datetime.datetime.now(), 'ecg_value': self.ECG}
            self.ecg_values.append(ecg_dict)

            flow_dict = {'date_time': datetime.datetime.now(), 'flow_value': self.flow}
            self.flow_values.append(flow_dict)

            # Insert every 50 values
            if(len(self.ecg_values)==50):
                self.insert_ecg_values(self.ecg_values)

            if(len(self.flow_values)==50):
                self.insert_flow_values(self.flow_values)


            # These needed to be added when these sensors are connected
            #self.stdout.write("Pressure reading..." + str(pressure))
            #self.stdout.write("Temperature reading..." + str(temperature))

            self.stdout.write("ECG reading..." + str(self.ECG))
            self.stdout.write("Flow reading..." + str(self.flow))

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type' : 'sensor_reading',
                    'ecg_value': self.ECG,
                    'bpm_value': round(self.BPM, 2),
                    'flow_value': round(self.flow, 2),
                    #'pressure_value': pressure,
                    #'temperature_value': temperature,
                }
            )
            # This can be changed based on how frequently sensors need to be read 
            time.sleep(0.5)
                  
    def take_ecg_reading(self):
        if (GPIO.input(22) == 1 and GPIO.input(27) ==1):
                print("Electrodes not connected")
        else:
            self.ECG = ECG_output.value
            print("ECG Connected, ECG: ", self.ECG)

    def insert_ecg_values(self, ecg_values):
        for value in (ecg_values):
            ecg = EcgData(user_id=self.user_id, date_time=value['date_time'], 
                ecg_value=value['ecg_value'])
            ecg.save()
        
    def insert_flow_values(self, flow_values):
         for value in (flow_values):
            flow = FlowData(user_id=self.user_id, date_time=value['date_time'], 
                flow_value=value['flow_value'])
            flow.save()

    def calculate_BPM(self):
        # get current time
        beat_new = int(round(time.time() * 1000))
        diff = beat_new - self.beat_old
        # convert to bpm
        currentBPM = 60000 / diff;   
        # store for average calculation
        self.beats[self.beatIndex] = currentBPM 
        total = sum(self.beats)
        BPM = total / 4
        self.beat_old = beat_new;
        if(self.beatIndex==3):
            self.beatIndex = 0
        else: 
            self.beatIndex = self.beatIndex + 1
        return float((0.5/0.024)*BPM)

        



        
import hashlib
import datetime
from sensorWorker.models import Session

class InsertSession():

    def __init__(self, origin_hospital, destination_hospital, start_date):
        self.origin_hospital = origin_hospital
        self.destination_hospital = destination_hospital
        self.start_date = start_date
        self.session_id = self.generate_session_id()


    def generate_session_id(self):
        input_string = self.origin_hospital + self.destination_hospital + str(self.start_date)
        hash_object = hashlib.sha1(input_string.encode())
        return hash_object.hexdigest()

    def insert_transport_session(self):
        s = Session(user_id=self.session_id, start_date=self.start_date, 
            origin=self.origin_hospital, destination=self.destination_hospital)
        s.save()

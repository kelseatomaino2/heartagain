import hashlib
import datetime
from sensorWorker.models import Session

class InsertSession():

    def __init__(self, origin_hospital, destination_hospital, start_date, notes=''):
        self.origin_hospital = origin_hospital
        self.destination_hospital = destination_hospital
        self.start_date = start_date
        self.notes = notes
        self.session_id = self.generate_session_id()


    def generate_session_id(self):
        input_string = self.origin_hospital + self.destination_hospital + str(self.start_date)
        hash_object = hashlib.sha1(input_string.encode())
        return hash_object.hexdigest()

    def insert_transport_session(self):
        s = Session(user_id=self.session_id, start_date=self.start_date, 
            origin=self.origin_hospital, destination=self.destination_hospital)
        s.save()

    def edit_transport_session(self, end_date, user_id, notes):
        s = Session.objects.filter(user_id__startswith=user_id).first()
        s.end_date = end_date
        s.notes = notes
        s.save()


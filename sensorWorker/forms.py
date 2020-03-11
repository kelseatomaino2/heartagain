from django import forms

class TransportForm(forms.Form):

    origin_hospital = forms.CharField(label='Origin Hospital', max_length=200)
    destination_hospital = forms.CharField(label='Destination Hospital', max_length=200)
    start_date = forms.DateTimeField(label="Start Date for Transport", required=False)
    notes = forms.CharField(label="Notes", max_length=400, required=False)

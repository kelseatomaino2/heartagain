from django import forms

class TransportForm(forms.Form):

    origin = forms.CharField(label='Origin Hospital', max_length=200)
    destination = forms.CharField(label='Destination Hospital', max_length=200)
    start_date = forms.DateTimeField(label="Start Date for Transport", required=False)
    notes = forms.CharField(label="Notes", max_length=400, required=False)

class FinishForm(forms.Form):
    origin = forms.CharField(label='Origin Hospital', max_length=200)
    destination = forms.CharField(label='Destination Hospital', max_length=200)
    start_date = forms.DateTimeField(label="Start Date for Transport", required=False)
    end_date = forms.DateTimeField(label="End Date for Transport", required=False)
    notes = forms.CharField(label="Notes", max_length=400, required=False)

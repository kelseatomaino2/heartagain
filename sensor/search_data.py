from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

class SearchData(forms.Form):

	user_id = forms.CharField(max_length=256, label="user_id")


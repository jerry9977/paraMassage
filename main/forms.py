from cProfile import label
from turtle import width
from django import forms
from django.db import models
from django.core.exceptions import ValidationError


import main.models as m
from main.widget import DatePickerInput, DateTimePickerInput, TimePickerInput
class CustomerCheckInForm(forms.ModelForm):
    mobile = forms.CharField(max_length=20, required=False, empty_value=None)
    home_phone = forms.CharField(max_length=20, required=False, empty_value=None)
    class Meta:
        model = m.Client
        fields = ["first_name", "last_name", "DOB", "email", "mobile", "home_phone"]

        widgets = {
            'DOB': DatePickerInput(),
        }

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "home_phone": "Home Phone"
        }

    def clean(self):
        
        cleaned_data = super(CustomerCheckInForm, self).clean()
        
        mobile = cleaned_data.get("mobile")
        home_phone = cleaned_data.get("home_phone")
        email = cleaned_data.get("email")

        if mobile is None and home_phone is None and email is None:

            raise ValidationError(message='Please provide at least one contact detail. Mobile, Email or Home Phone')





class RemedialCheckInForm(forms.ModelForm):
    class Meta:
        model = m.RemedialMedicalHistory
        fields = '__all__'
        exclude = ['remedial_client_info']

        

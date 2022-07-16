from turtle import width
from django.forms import ModelForm

import main.models as m
from main.widget import DatePickerInput, DateTimePickerInput, TimePickerInput
class CustomerCheckInForm(ModelForm):
    class Meta:
        model = m.Client
        fields = ["first_name", "last_name", "DOB", "email", "mobile", "home_phone"]

        widgets = {
            'DOB': DatePickerInput()
        }
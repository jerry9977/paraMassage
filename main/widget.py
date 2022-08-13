from django import forms
from django.db import models
class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class CustomImageField(forms.ImageField):
    
    attrs={"sore_area_front":True,"input_type":"hidden"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def id_for_label(self, value):
        return ""

    def to_python(self, value):
        print("===================")
        print("===================")
        print("========pyhthon===========")
        print("===================")
        print(value)
        return ""
    
    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        print("===123=")
        print(data)
        print(files)
        print(name)
        return data.get(name)
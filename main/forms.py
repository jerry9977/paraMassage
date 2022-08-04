from django import forms
from django.db import models
from django.core.exceptions import ValidationError


import main.models as m
from main.widget import DatePickerInput, DateTimePickerInput, TimePickerInput

GENDER_CHOICES = [
    (0, ""),
    (1, "Male"),
    (2, "Female"),
    (3, "Prefer not to say")
]

MARTIAL_STATUS_CHOICES = [
    (0, ""),
    (1, "Married"),
    (2, "Widowed"),
    (3, "Separated"),
    (4, "Divorced"),
    (5, "Single"),
    (6, "Prefer not to say")
]

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


class RemedialCustomerCheckInForm(forms.ModelForm):
    health_insurance_number = forms.CharField(max_length=20)
    suffix = forms.CharField(max_length=4)
    # gender = forms.Select(choices=GENDER_CHOICES)
    # martial_status = forms.Select(choices=MARTIAL_STATUS_CHOICES)
    class Meta:
        model = m.RemedialClientInfo
        fields = '__all__'
        exclude = ['client']
        widgets = {
            "gender": forms.Select(choices=GENDER_CHOICES),
            "martial_status" : forms.Select(choices=MARTIAL_STATUS_CHOICES)
        }


class RemedialHistoryForm(forms.ModelForm):
     
    class Meta:
        model = m.RemedialMedicalHistory
        fields = '__all__'
        exclude = ['remedial_client_info']

        widgets = {
            'area_of_soreness': forms.Textarea(attrs={"sore_area":True,"input_type":"textarea"}),
            # 'area_of_soreness_back': forms.Textarea(attrs={"sore_area":True,"input_type":"textarea"}),
            'reason_of_visit': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'medication': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'health_care': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'signature': forms.Textarea(attrs={"signature":True,"input_type":"textarea"}),
            'additional_comments': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"})
        }

        

from django import forms
from django.db import models
from django.core.exceptions import ValidationError


import main.models as m
from main.widget import DatePickerInput, DateTimePickerInput, TimePickerInput, CustomImageField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
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
        fields = ["email", "mobile", "home_phone", "first_name", "last_name", "DOB"]

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
    # suffix = forms.CharField(max_length=4)
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
    # captcha = ReCaptchaField(
    #     widget=ReCaptchaV3(
    #     attrs={
    #         'required_score':0,
    #         'recaptcha': True,
    #         'input_type': "hidden"
    #     }
    # ))

    class Meta:
        model = m.RemedialMedicalHistory
        fields = '__all__'
        exclude = ['remedial_client_info', 'receipt_image', 'remedial_treatment_plan']

        widgets = {
            'area_of_soreness_front': forms.TextInput(attrs={"sore_area_front":True,"input_type":"hidden"}),
            'area_of_soreness_back': forms.TextInput(attrs={"sore_area_back":True,"input_type":"hidden"}),
            'reason_of_visit': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'medication': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'health_care': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'signature': forms.TextInput(attrs={"signature":True,"input_type":"hidden"}),
            'additional_comments': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"})
        }


    # def clean(self):
    #     cleaned_data = super().clean()
    #     print("====================")
    #     print("====================")
    #     print("====================")
    #     print("====================")
    #     print(cleaned_data)
    # def clean_area_of_soreness(self):
    #     print("=========================")
    #     print("=========================")
    #     print("=========================")
    #     print(self.cleaned_data)
    #     # print(self)
    #     # data = self.cleaned_data["area_of_soreness"]
    #     pass

        

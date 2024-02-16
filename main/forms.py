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

YES_NO = [
    (0, "No"),
    (1, "Yes")
]

class CustomerCheckInForm(forms.ModelForm):
    class Meta:
        model = m.Client
        fields = [
            "first_name", 
            "last_name", 
            "health_insurance_number",
            "reference_number",
            "email",
            "DOB",
            "phone_day", 
            "phone_night",
        ]

        widgets = {
            'DOB': DatePickerInput(),
        }


    def clean(self):
        pass
        # cleaned_data = super(CustomerCheckInForm, self).clean()
        
        # phone_day = cleaned_data.get("phone_day")
        # phone_night = cleaned_data.get("phone_night")
        # email = cleaned_data.get("email")

        # if phone_day is None and phone_night is None and email is None:

        #     raise ValidationError(message='Please provide at least one contact detail. Email or Phone (Day or Evening)')


class DetailedClientForm(forms.ModelForm):
    class Meta:
        model = m.ClientDetailInfo
        fields = [
            "address", 
            "suburb",
            "state",
            "post_code",
            "occupation",
            "employer",
            "primary_physician",
            "emergency_contact_name",
            "emergency_contact_number",
            "emergency_contact_relation",
            "hear_about_us"
        ]
        exclude = ['client']

        labels = {
            "primary_physician": "Primary Physician",
            "emergency_contact_name": "Emergency Contact Name",
            "emergency_contact_number": "Emergency Contact Number",
            "emergency_contact_relation": "Emergency Contact Relation",
            "hear_about_us": "How did you hear about us ?"
        }


class ClientMedicalHistoryForm(forms.ModelForm):


    class Meta:
        model = m.ClientMedicalHistory
        fields = [
            "medication",
            "medication_detail",

            "pregnant",
            "pregnant_time",
            "pregnant_factor",

            "chronic_pain",
            "chronic_pain_detail",
            "chronic_pain_better",
            "chronic_pain_worse",

            "orthopedic_injuries",
            "orthopedic_injuries_detail",

            "conditions",
            "conditions_detail",

            "professional_massage",

            "massage_type",
            "massage_type_other",

            "pressure_preference",

            "allergies",
            "allergies_detail",

            "no_massage_area",
            "no_massage_area_detail",

            "reason_of_visit",
            'area_of_soreness_front',
            'area_of_soreness_back',
            'area_of_soreness_left',
            'area_of_soreness_right',
            "signature",

        ]
        exclude = ['detail_client_info', 'receipt_image', 'remedial_treatment_plan']
        widgets = {
            # "medication": forms.RadioSelect(choices=YES_NO),
            # 'medication_detail': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            'area_of_soreness_front': forms.TextInput(),
            'area_of_soreness_back': forms.TextInput(),
            # 'area_of_soreness_left': forms.TextInput(attrs={"sore_area_left":True,"input_type":"hidden"}),
            # 'area_of_soreness_right': forms.TextInput(attrs={"sore_area_right":True,"input_type":"hidden"}),
            # 'reason_of_visit': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            # 'health_care': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"}),
            # 'signature': forms.TextInput(attrs={"signature":True,"input_type":"hidden"}),
            # 'additional_comments': forms.Textarea(attrs={"input_type":"textarea", "rows":"5"})
        }


    def clean_area_of_soreness_front(self):
        front = self.cleaned_data['area_of_soreness_front']
        
        return front
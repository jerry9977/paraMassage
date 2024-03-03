
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from main.image_verifier.image_verifier import ImageVerifier
from main.widget import DatePickerInput, DateTimePickerInput, TimePickerInput, CustomImageField

import main.models as m
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
            "gender",
            "health_fund",
            "health_insurance_number",
            "reference_number",
            "email",
            "DOB",
            "phone_day",
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
            "emergency_contact_name",
            "emergency_contact_number",
            "hear_about_us"
        ]
        exclude = ['client']



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

            "orthopedic_injuries",
            "orthopedic_injuries_detail",

            "conditions",
            "conditions_detail",

            "pressure_preference",

            "no_massage_area",
            "no_massage_area_detail",

            "area_of_soreness",
            "signature",

        ]
        exclude = ['detail_client_info', 'receipt_image', 'remedial_treatment_plan']
        widgets = {
            'area_of_soreness': forms.TextInput(),
        }


    def clean_area_of_soreness(self):
        image = self.data['area_of_soreness_hidden']
        image_verifier = ImageVerifier(image, allow_null=True)
        if image_verifier.is_valid():
            # print(image)
            return image
        raise ValidationError(message='Internal Server Error')
    
    def clean_signature(self):
        image = self.data['signature_hidden']
        image_verifier = ImageVerifier(image, allow_null=False)
        if image_verifier.is_valid():
            return image
        raise ValidationError(message='Internal Server Error')


class SimpleMedicalHistoryForm(forms.ModelForm):


    class Meta:
        model = m.ClientMedicalHistory
        fields = [

            "area_of_soreness",
            "signature",

        ]
        exclude = ['detail_client_info', 'receipt_image', 'remedial_treatment_plan']
        widgets = {
            'area_of_soreness': forms.TextInput(),
        }


    def clean_area_of_soreness(self):
        image = self.data['area_of_soreness_hidden']
        image_verifier = ImageVerifier(image, allow_null=True)
        if image_verifier.is_valid():
            # print(image)
            return image
        raise ValidationError(message='Internal Server Error')
    
    def clean_signature(self):
        image = self.data['signature_hidden']
        image_verifier = ImageVerifier(image, allow_null=False)
        if image_verifier.is_valid():
            return image
        raise ValidationError(message='Internal Server Error')
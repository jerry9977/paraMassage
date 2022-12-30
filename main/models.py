
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from multiselectfield import MultiSelectField

import datetime
# Create your models here.



    
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    remote_addr = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def handle_duplicate_logins(self):

        twelve_hours_before = datetime.datetime.now() - datetime.timedelta(hours=12)

        session_keys = LoginHistory.objects.filter(user=self.user, login_time__gte=twelve_hours_before).values_list("session_key", flat=True)

        Session.objects.filter(session_key__in=session_keys).delete()
    

class Client(models.Model):
    class Meta:
        db_table = 'core_client'
    

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=True, blank=True, unique=True)
    DOB = models.DateField(null=True, blank=True)
    
    mobile = models.TextField(   
        null=True, 
        blank=True, 
        unique=True, 
        max_length=20, 
        error_messages={
            "invalid":"Please enter only digits"
        }
    )

    home_phone = models.TextField(   
        null=True, 
        blank=True, 
        unique=True, 
        max_length=20, 
        error_messages={
            "invalid":"Please enter only digits"
        }
    )
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name

    def clean(self):
        if self.mobile is None and self.home_phone is None and self.email is None:
            raise ValidationError({
                "mobile":ValidationError(message=''),
                "home_phone":ValidationError(message=''),
                "email":ValidationError(message='')
            })
        
        
            
class RemedialClientInfo(models.Model):
    class Meta:
        db_table = 'core_remedial_client_info'
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    health_insurance_number = models.TextField(
        null=False, 
        blank=False,
        max_length=25, 
        error_messages={
            "invalid":"Please enter only digits"
        }
    )

    suffix = models.TextField(
        null=True, 
        blank=True,
        max_length=4,
        error_messages={
            "invalid":"Please enter only digits"
        }
    )

    gender = models.IntegerField(null=True, blank=True)
    martial_status = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=500, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=300, decimal_places=2, null=True, blank=True)
    
    children = models.IntegerField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    job = models.TextField(null=True, blank=True)
    emergency_contact_number = models.TextField(null=True, blank=True, max_length=20)
    emergency_contact_name = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client.first_name


SYMPTOM_CHOICES = (
    (1, "CHRONIC PAIN"),
    (2, "HEADACHES"),
    (3, "COLD / FLU / FEVER"),
    (4, "DIABETES"),
    (5, "HEART AILMENTS"),
    (6, "KIDNEY AILMENTS"),
    (7, "CANCER"),
    (8, "INFECTIOUS CONDITIONS"),
    (9, "HERPES"),
    (10, "SHINGLES"),
    (11, "ECZEMA"),
    (12, "PSORIASIS"),
    (13, "SKIN DISORDERS"),
    (14, "AIDS"),
    (15, "PHLEBITIS"),
    (16, "VARICOSE VEINS"),
    (17, "JOINT REPLACEMENTS"),
    (18, "BLOOD CLOTS"),
    (19, "TMJ SYNDROME"),
    (20, "NECK OR SPINE INJURY"),
    (21, "NUMBNESS"),
    (22, "FATIGUE"),
    (23, "DEPRESSION"),
    (24, "NERVOUSNESS"),
    (25, "DIZZINESS"),
    (26, "ALLERGIES"),
    (27, "ARTHRITIS"),
    (28, "EPILEPSY"),
    (29, "INSOMNIA"),
    (30, "PREGNANCY"),
    (31, "PMS SYNDROME"),
    (32, "SLEEP DISORDERS"),
    (33, "OTHER")
)


class RemedialMedicalHistory(models.Model):
    class Meta:
        db_table = 'core_remedial_medical_history'
    remedial_client_info = models.ForeignKey(RemedialClientInfo, on_delete=models.CASCADE)
    area_of_soreness_front = models.ImageField(upload_to='area_of_soreness/%Y/%m/%d/', null=True, blank=True)
    area_of_soreness_back = models.ImageField(upload_to='area_of_soreness/%Y/%m/%d/', null=True, blank=True)

    reason_of_visit = models.TextField(null=True, blank=True, max_length=500)
    symptoms = MultiSelectField(choices=SYMPTOM_CHOICES, null=True, blank=True)
    medication = models.TextField(
        null=True, 
        blank=True, 
        max_length=500,
        verbose_name="Are you currently taking any medication? If so please provide the medication name."
    )
    health_care = models.TextField(
        null=True, 
        blank=True, 
        max_length=500,
        verbose_name="Are you currently under the care of a health care professional? If so please provide physicians name and phone number."
    )

    additional_comments = models.TextField(
        null=True,
        blank=True,
        max_length=500,
    )

    remedial_treatment_plan = models.TextField(
        null=True,
        blank=True
    )


    signature = models.ImageField(upload_to='signature/%Y/%m/%d/', null=False, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    receipt_image = models.ImageField(upload_to='receipt/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return str(self.id)

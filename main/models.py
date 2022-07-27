
from django.db import models
from django.core.exceptions import ValidationError

from jsignature.fields import JSignatureField
# Create your models here.


class Client(models.Model):
    class Meta:
        db_table = 'core_client'
    

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    DOB = models.DateField(null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True, unique=True)
    home_phone = models.IntegerField(null=True, blank=True, unique=True)
    date_created = models.DateField()

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
    gender = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=500, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=300, decimal_places=2, null=True, blank=True)
    martial_status = models.TextField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    emergency_contact_number = models.IntegerField(null=True, blank=True)
    emergency_contact_name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.client.first_name
class RemedialMedicalHistory(models.Model):
    pass
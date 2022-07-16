from tkinter import CASCADE
from turtle import home
from django.db import models

# Create your models here.


class Client(models.Model):
    class Meta:
        db_table = 'core_client'
    

    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField()
    DOB = models.DateField()
    mobile = models.IntegerField()
    home_phone = models.IntegerField()

    def __str__(self):
        return self.first_name

class RemedialClientInfo(models.Model):
    class Meta:
        db_table = 'core_remedial_client_info'
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    gender = models.TextField()
    weight = models.DecimalField(max_digits=500, decimal_places=2)
    height = models.DecimalField(max_digits=300, decimal_places=2)
    martial_status = models.TextField()
    children = models.IntegerField()
    occupation = models.TextField()
    address = models.TextField()

    emergency_contact_number = models.IntegerField()
    emergency_contact_name = models.TextField()


class RemedialMedicalHistory(models.Model):
    pass
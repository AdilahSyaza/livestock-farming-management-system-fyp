from datetime import date
from django.db import models

# Create your models here.

# This model defines User table in database with fields related to user information.
class User(models.Model):

    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    staffID = models.CharField(max_length=150)
    username = models.CharField(max_length=150, null=True)
    firstName = models.CharField(max_length=150, null=True)
    lastName = models.CharField(max_length=150, null=True)
    gender = models.CharField(max_length=150)
    dateOfBirth = models.DateField(null=True)
    address = models.CharField(max_length=150, null=True)
    maritalStatus = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    reasonDeactivation = models.CharField(max_length=150, default="Not Applicable", null=True)
    userRole = models.CharField(max_length=150)
    dateJoined = models.DateField(default=date.today)
    media = models.ImageField(upload_to='uploads/',default="", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'User'

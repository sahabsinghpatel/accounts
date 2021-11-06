from django.db import models

class Temp_User(models.Model):
    username=models.CharField(max_length=100, blank=True)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=40, blank=True)
    otp=models.IntegerField()
    token=models.CharField(max_length=65)
    time=models.TimeField(auto_now_add=True)

from django.db import models

# Create your models here.
class WebUser (models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    psw_md5 = models.CharField(max_length=32)
    salt = models.CharField(max_length=6)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=11,blank=True)



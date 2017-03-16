from django.db import models

# Create your models here.
class TGR2017(models.Model):
    id = models.AutoField
    temperature = models.CharField(max_length=5)
    weather = models.CharField(max_length=50)
    pressure = models.FloatField
    humidity = models.FloatField
    picture = models.TextField
    created = models.DateField
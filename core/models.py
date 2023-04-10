from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to= 'dog')
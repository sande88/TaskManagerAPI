from django.db import models

# Create your models here.

class tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    priority = models.CharField(max_length=15)
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.title

    

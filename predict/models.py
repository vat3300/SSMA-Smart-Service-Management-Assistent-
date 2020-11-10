from django.db import models

class PredResults(models.Model):

    message = models.CharField(max_length=3000)
    response = models.CharField(max_length=30)
    response1 = models.CharField(max_length=30)
    response2 = models.CharField(max_length=30)


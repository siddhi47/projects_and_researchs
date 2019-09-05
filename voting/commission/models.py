from django.db import models

class Vote(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    account = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name
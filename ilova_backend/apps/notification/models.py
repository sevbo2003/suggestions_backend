from django.db import models


class Mahalla(models.Model):
    district = models.CharField(max_length=100)
    mahalla = models.CharField(max_length=100)

    def __str__(self):
        return self.district + " " + self.mahalla
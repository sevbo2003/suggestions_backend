from django.db import models
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField, ShortUUID
from core.geo_finder import get_location

User = get_user_model()


class ProblemType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ariza turi"
        verbose_name_plural = "Ariza turlari"


class Status(models.TextChoices):
    SOLVED = "Muvaffaqiyatli"
    PENDING = "Kutilmoqda"
    FAKE = "Yolg'on"


class Location(models.Model):
    lon = models.DecimalField(max_digits=24, decimal_places=22)
    lat = models.DecimalField(max_digits=24, decimal_places=22)

    def __str__(self) -> str:
        return f"{self.lon} + {self.lat}"


class Problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_problems")
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    images = models.FileField(upload_to="%Y/%m/%d/")
    date = models.DateTimeField(auto_now_add=True)
    problem_types = models.ManyToManyField(ProblemType, related_name="problems")
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PENDING)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="problems")

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ["-date"]
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
    
    def save(self, *args, **kwargs):
        self.city, self.district = get_location(str(self.location.lon), str(self.location.lat))
        super().save(*args, **kwargs)

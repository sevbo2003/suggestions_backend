from django.db import models


class Mahalla(models.Model):
    district = models.CharField(max_length=100)
    mahalla = models.CharField(max_length=100)

    def __str__(self):
        return self.district + " " + self.mahalla


class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='notification/images/', blank=True, null=True)
    mahalla = models.ManyToManyField(Mahalla, related_name="notification")
    date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Xabarnomalar"
        verbose_name = "Xabarnoma"
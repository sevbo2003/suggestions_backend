from django.db import models
from apps.suggestions.models import Problem


class Message(models.Model):
    from_problem_user = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='from_user')
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]
    
    class Meta:
        ordering = ('-date',)
    
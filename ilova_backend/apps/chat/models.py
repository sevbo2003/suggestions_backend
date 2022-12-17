from django.db import models
from apps.suggestions.models import Problem


class SenderType(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'


class ChatProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='chat_problem')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def last_message(self):
        return self.messages.first().message if self.messages.first() else None
    
    @property
    def user(self):
        return self.problem.user

    def __str__(self):
        return self.problem.description[:20]
    
    class Meta:
        ordering = ('-created_at',)


class Message(models.Model):
    chat_problem = models.ForeignKey(ChatProblem, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=1000)
    file = models.FileField(upload_to='files/messages', blank=True, null=True)
    sender = models.CharField(max_length=10, choices=SenderType.choices)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]
    
    class Meta:
        ordering = ('-date',)
    

class MessageFile(models.Model):
    file = models.FileField(upload_to='files/messages')

    def __str__(self):
        return self.file.name
    
    def get_url(self):
        return self.file.url

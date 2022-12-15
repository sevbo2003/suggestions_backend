from django.db import models
from apps.suggestions.models import Problem


class ChatProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='chat_problem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem.description[:20]
    
    class Meta:
        ordering = ('-created_at',)


class Message(models.Model):
    chat_problem = models.ForeignKey(ChatProblem, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]
    
    class Meta:
        ordering = ('-date',)
        
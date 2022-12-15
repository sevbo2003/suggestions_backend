from django.contrib import admin

# Register your models here.
from .models import Message, ChatProblem

admin.site.register(Message)
admin.site.register(ChatProblem)
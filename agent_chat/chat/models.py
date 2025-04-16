# chat/models.py

from django.db import models
from django.contrib.auth.models import User

class HistoricalFigure(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField(help_text="系统消息，用于引导AI角色")

    def __str__(self):
        return self.name

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    historical_figure = models.ForeignKey(HistoricalFigure, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.historical_figure.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Message(models.Model):
    SENDERS = (
        ('user', '用户'),
        ('assistant', 'AI'),
    )
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDERS)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.content[:50]}"

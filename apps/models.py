# events/models.py
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']  # Most recent events first
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['location']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.title} ({self.date})"

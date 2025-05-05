# Register your models here.
from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created_by', 'created_at')
    list_filter = ('date', 'location', 'created_by')
    search_fields = ('title', 'description', 'location', 'created_by__username')
    ordering = ('-date',)

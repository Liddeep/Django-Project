from django.contrib import admin
from .models import ControlPanel, ChatSessions

# Register your models here.

@admin.register(ControlPanel)
class ControlPanel(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'updated_at')
    list_filter = ('is_active', 'user')
    search_fields = ('name', 'description')

@admin.register(ChatSessions)
class Chats(admin.ModelAdmin):
    list_display = ('title', 'user', 'panel', 'created_at', 'last_activity')
    list_filter = ('panel', 'user')
    search_fields = ('title',)
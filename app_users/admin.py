from django.contrib import admin
from .models import Profil, Message, Notification

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'statut', 'created_at')
    list_filter = ('role', 'statut')
    search_fields = ('user__username', 'user__email')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'dateEnvoi', 'lu')
    list_filter = ('lu', 'dateEnvoi')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'dateEnvoi', 'lu')
    list_filter = ('lu', 'dateEnvoi')
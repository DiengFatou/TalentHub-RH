from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InscriptionViewSet, MessageViewSet, ModifierUtilisateurView, MonProfilViewSet, NotificationViewSet

# Création du routeur
router = DefaultRouter()
router.register(r'inscription', InscriptionViewSet, basename='inscription')
router.register(r'profil', MonProfilViewSet, basename='profil')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'notifications', NotificationViewSet, basename='notifications')
    
urlpatterns = [
    path('', include(router.urls)), 
    path('utilisateur/modifier/', ModifierUtilisateurView.as_view(), name='modifier-utilisateur'),
]
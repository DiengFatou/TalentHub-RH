from django.db import models
from django.contrib.auth.models import User  # On utilise l'utilisateur de Django

# 1. Le modèle Profil (attaché à l'utilisateur Django)
class Profil(models.Model):
    # Lien obligatoire avec l'utilisateur de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')

    # Vos champs spécifiques (provenant de votre diagramme UML)
    numCni = models.CharField(max_length=50, blank=True, null=True)
    dateNaissance = models.DateField(blank=True, null=True)
    lieuNaissance = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    numPassport = models.CharField(max_length=50, blank=True, null=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)
    
    # Le rôle (Candidat, Recruteur, Admin)
    ROLE_CHOICES = (
        ('candidat', 'Candidat'),
        ('recruteur', 'Recruteur'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidat')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
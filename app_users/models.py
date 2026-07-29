from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')

    # Champs communs
    numCni = models.CharField(max_length=50, blank=True, null=True, unique=True, db_index=True)
    dateNaissance = models.DateField(blank=True, null=True)
    lieuNaissance = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True, unique=True, db_index=True)
    numPassport = models.CharField(max_length=50, blank=True, null=True, unique=True, db_index=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Le rôle (Candidat, Recruteur, Admin)
    ROLE_CHOICES = (
        ('candidat', 'Candidat'),
        ('recruteur', 'Recruteur'),
        ('freelance', 'Freelance')

    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidat')

    # Champs spécifiques Candidat
    niveauEtude = models.CharField(max_length=100, blank=True, null=True)
    dernierDiplome = models.CharField(max_length=100, blank=True, null=True)
    dateObtentionDiplome = models.DateField(blank=True, null=True)
    nationalite = models.CharField(max_length=50, blank=True, null=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=50, default='Actif')

    # Champs spécifiques Recruteur
    dateEmbauche = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Message(models.Model):
    contenu = models.TextField()
    dateEnvoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username}"


class Notification(models.Model):
    contenu = models.TextField()
    dateEnvoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notif pour {self.destinataire.username}"
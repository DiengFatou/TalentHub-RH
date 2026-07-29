from django.db import models
from django.contrib.auth.models import User
from app_offres.models import Offre

class Candidature(models.Model):
    dateSoumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default='En attente')
    dateModification = models.DateTimeField(auto_now=True)
    
    # Relations
    candidat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidatures')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')
    class Meta:
        # Cette contrainte empêche un même candidat de postuler plusieurs fois à la même offre
        constraints = [
            models.UniqueConstraint(
                fields=['candidat', 'offre'],
                name='unique_candidature_par_offre'
            )
        ]

    
    def __str__(self):
        return f"Candidature de {self.candidat.username} pour {self.offre.titre}"


class Document(models.Model):
    nomFichier = models.CharField(max_length=200)
    typeFichier = models.CharField(max_length=50)  # PDF, DOCX, JPG...
    contenu = models.FileField(upload_to='documents/%Y/%m/%d/')
    taille = models.IntegerField(default=0)
    lien = models.URLField(blank=True, null=True)
    
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomFichier


class Entretien(models.Model):
    dateHeure = models.DateTimeField()
    type = models.CharField(max_length=50)  # Visio, Presentiel, Telephonique
    lieu = models.CharField(max_length=200, blank=True, null=True)
    statut = models.CharField(max_length=50, default='Planifié')
    
    recruteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entretiens_animes')
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE, related_name='entretiens')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entretien {self.type} le {self.dateHeure}"
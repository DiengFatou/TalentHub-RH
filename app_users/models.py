from django.db import models
from django.contrib.auth.models import AbstractUser

# ------------------------------------------------------------------
# 1. CLASSE ABSTRAITE PERSONNE (Héritage)
# ------------------------------------------------------------------
class Personne(AbstractUser):
    # AbstractUser contient déjà : username, password, email, first_name, last_name
    # Nous ajoutons les champs spécifiques de votre diagramme
    numCni = models.CharField(max_length=50, blank=True, null=True)
    dateNaissance = models.DateField(blank=True, null=True)
    lieuNaissance = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    numPassport = models.CharField(max_length=50, blank=True, null=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)
    
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('recruteur', 'Recruteur'),
        ('candidat', 'Candidat'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidat')

    class Meta:
        abstract = True  # Ceci empêche la création d'une table "Personne" dans la DB

    def __str__(self):
        return f"{self.username} ({self.role})"


# ------------------------------------------------------------------
# 2. CLASSES FILLES (Héritage de Personne)
# ------------------------------------------------------------------
class Administrateur(Personne):
    service = models.CharField(max_length=100)
    niveauAcces = models.IntegerField(default=1)

    # La méthode est gérée par le code des vues (views.py), pas dans le modèle
    def validerOffre(self):
        pass

    def genererRapport(self):
        pass


class Recruteur(Personne):
    dateEmbauche = models.DateField()
    # Note : La relation avec Entreprise est gérée plus bas avec une clé étrangère

    def publierOffre(self):
        pass


class Candidat(Personne):
    niveauEtude = models.CharField(max_length=100)
    nombreDiplomes = models.IntegerField(default=0)
    dateObtentionDiplome = models.DateField(blank=True, null=True)
    nationalite = models.CharField(max_length=50)
    specialite = models.CharField(max_length=100)
    type = models.CharField(max_length=50, help_text="Ex: Etudiant, Professionnel")

    def postuler(self):
        pass


# ------------------------------------------------------------------
# 3. CLASSES ENTIÉTÉS (RELATIONS)
# ------------------------------------------------------------------
class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    secteur = models.CharField(max_length=100)
    adresse = models.TextField()
    siteweb = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Offre(models.Model):
    titre = models.CharField(max_length=200)
    datePublication = models.DateTimeField(auto_now_add=True)
    dateLimite = models.DateField()
    typeOffre = models.CharField(max_length=50)  # CDI, Stage, Freelance...
    description = models.TextField()
    
    # Relations
    # Un recruteur publie une offre
    recruteur = models.ForeignKey(Recruteur, on_delete=models.CASCADE, related_name='offres_publices')
    # L'offre appartient à une entreprise (via le recruteur, ou directement)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='offres')

    def FermerOffre(self):
        pass

    def __str__(self):
        return self.titre


class Competence(models.Model):
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)  # Ex: "Débutant", "Avancé"

    def __str__(self):
        return self.nom


# CLASSE D'ASSOCIATION (Lien entre Offre et Competence, et Candidat et Competence)
class NiveauCompetence(models.Model):
    # Attributs de l'association
    niveauRequis = models.CharField(max_length=50)
    anneesExperience = models.IntegerField(default=0)
    
    # Clés étrangères vers les classes reliées
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='competences_requises', blank=True, null=True)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='competences_possessees', blank=True, null=True)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competence.nom} - Niveau: {self.niveauRequis}"


class Candidature(models.Model):
    dateSoumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default='En attente') # Envoyée, En cours, Acceptée, Rejetée
    dateModification = models.DateTimeField(auto_now=True)
    
    # Relations
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='candidatures')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')

    def ChangerStatut(self):
        pass

    def __str__(self):
        return f"Candidature de {self.candidat.username} pour {self.offre.titre}"


class Entretien(models.Model):
    dateHeure = models.DateTimeField()
    type = models.CharField(max_length=50)  # Visio, Presentiel, Telephonique
    
    # Relations
    recruteur = models.ForeignKey(Recruteur, on_delete=models.CASCADE)
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE)

    def Confirmer(self):
        pass

    def __str__(self):
        return f"Entretien {self.type} le {self.dateHeure}"


class Notification(models.Model):
    contenu = models.TextField()
    dateEnvoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    # Relations
    destinataire = models.ForeignKey(Personne, on_delete=models.CASCADE)  # Note: Ceci fonctionne car Personne est une classe abstraite pour les classes filles

    def Envoyer(self):
        pass

    def __str__(self):
        return f"Notification pour {self.destinataire.username}"


class Document(models.Model):
    nomFichier = models.CharField(max_length=200)
    typeFichier = models.CharField(max_length=50)
    contenu = models.FileField(upload_to='documents/')  # Pour stocker le fichier physique
    emplacement = models.CharField(max_length=255, blank=True, null=True) # Chemin de stockage supplémentaire
    
    # Relations
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE, related_name='documents')
from django.conf import settings
from django.db import models

from apps.core.models import AssetModel, Location, Manufacturer


class AssetType(models.Model):
    nom = models.CharField("Type d'actif", max_length=120, unique=True)

    class Meta:
        verbose_name = "Type d'actif"
        verbose_name_plural = "Types d'actifs"

    def __str__(self):
        return self.nom


class Equipement(models.Model):
    STATUS_CHOICES = [
        ("ONLINE", "En ligne"),
        ("OFFLINE", "Hors ligne"),
        ("NO_TRACK", "Non suivi"),
    ]

    CRIT_CHOICES = [
        ("CRITIQUE", "Critique"),
        ("IMPORTANT", "Important"),
        ("NORMAL", "Normal"),
    ]

    nom = models.CharField("Nom", max_length=200)
    designation = models.CharField("Designation", max_length=200, blank=True)
    code_gmao = models.CharField("Code/QR GMAO", max_length=64, unique=True, db_index=True)
    id_externe = models.CharField("ID externe (optionnel)", max_length=64, blank=True)

    localisation = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="equipements",
        verbose_name="Localisation",
    )
    asset_type = models.ForeignKey(
        AssetType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipements",
        verbose_name="Type d'actif",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sous_actifs",
        verbose_name="Actif parent",
    )
    fabricant = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipements",
        verbose_name="Fabricant",
    )
    modele = models.ForeignKey(
        AssetModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipements",
        verbose_name="Modele",
    )

    numero_serie = models.CharField("Numero de serie", max_length=120, blank=True)
    annee = models.CharField("Annee", max_length=4, blank=True)
    description = models.TextField("Description", blank=True)
    status = models.CharField("Statut", max_length=10, choices=STATUS_CHOICES, default="ONLINE")
    criticalite = models.CharField("Criticite", max_length=10, choices=CRIT_CHOICES, default="NORMAL")

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Cree par",
    )
    cree_le = models.DateTimeField("Cree le", auto_now_add=True)
    modifie_le = models.DateTimeField("Modifie le", auto_now=True)
    supprime_le = models.DateTimeField("Supprime le", null=True, blank=True)

    class Meta:
        ordering = ("nom",)
        verbose_name = "Equipement"
        verbose_name_plural = "Equipements"

    def __str__(self):
        return f"{self.nom} ({self.code_gmao})"


class EquipementImage(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="equipements/images/")
    titre = models.CharField(max_length=140, blank=True)

    class Meta:
        verbose_name = "Image d'equipement"
        verbose_name_plural = "Images d'equipement"


class EquipementFichier(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="fichiers")
    fichier = models.FileField(upload_to="equipements/fichiers/")
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Fichier d'equipement"
        verbose_name_plural = "Fichiers d'equipement"

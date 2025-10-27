from django.db import models


class Site(models.Model):
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Location(models.Model):
    nom = models.CharField("Nom du lieu", max_length=200, unique=True)

    class Meta:
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"

    def __str__(self):
        return self.nom


class Manufacturer(models.Model):
    nom = models.CharField("Fabricant", max_length=200, unique=True)

    class Meta:
        verbose_name = "Fabricant"
        verbose_name_plural = "Fabricants"

    def __str__(self):
        return self.nom


class AssetModel(models.Model):
    fabricant = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="modeles")
    nom = models.CharField("Modele", max_length=200)

    class Meta:
        unique_together = ("fabricant", "nom")
        verbose_name = "Modele d'equipement"
        verbose_name_plural = "Modeles d'equipement"

    def __str__(self):
        return f"{self.fabricant} - {self.nom}"

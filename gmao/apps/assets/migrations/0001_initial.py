"""Generated initial migration for assets app."""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_location_manufacturer_assetmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=120, unique=True, verbose_name="Type d'actif")),
            ],
            options={
                "verbose_name": "Type d'actif",
                "verbose_name_plural": "Types d'actifs",
            },
        ),
        migrations.CreateModel(
            name="Equipement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=200, verbose_name="Nom")),
                ("designation", models.CharField(blank=True, max_length=200, verbose_name="Designation")),
                ("code_gmao", models.CharField(db_index=True, max_length=64, unique=True, verbose_name="Code/QR GMAO")),
                ("id_externe", models.CharField(blank=True, max_length=64, verbose_name="ID externe (optionnel)")),
                ("numero_serie", models.CharField(blank=True, max_length=120, verbose_name="Numero de serie")),
                ("annee", models.CharField(blank=True, max_length=4, verbose_name="Annee")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                (
                    "status",
                    models.CharField(
                        choices=[("ONLINE", "En ligne"), ("OFFLINE", "Hors ligne"), ("NO_TRACK", "Non suivi")],
                        default="ONLINE",
                        max_length=10,
                        verbose_name="Statut",
                    ),
                ),
                (
                    "criticalite",
                    models.CharField(
                        choices=[("CRITIQUE", "Critique"), ("IMPORTANT", "Important"), ("NORMAL", "Normal")],
                        default="NORMAL",
                        max_length=10,
                        verbose_name="Criticite",
                    ),
                ),
                ("cree_le", models.DateTimeField(auto_now_add=True, verbose_name="Cree le")),
                ("modifie_le", models.DateTimeField(auto_now=True, verbose_name="Modifie le")),
                ("supprime_le", models.DateTimeField(blank=True, null=True, verbose_name="Supprime le")),
                (
                    "asset_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="equipements",
                        to="assets.assettype",
                        verbose_name="Type d'actif",
                    ),
                ),
                (
                    "cree_par",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Cree par",
                    ),
                ),
                (
                    "fabricant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="equipements",
                        to="core.manufacturer",
                        verbose_name="Fabricant",
                    ),
                ),
                (
                    "localisation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="equipements",
                        to="core.location",
                        verbose_name="Localisation",
                    ),
                ),
                (
                    "modele",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="equipements",
                        to="core.assetmodel",
                        verbose_name="Modele",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sous_actifs",
                        to="assets.equipement",
                        verbose_name="Actif parent",
                    ),
                ),
            ],
            options={
                "ordering": ("nom",),
                "verbose_name": "Equipement",
                "verbose_name_plural": "Equipements",
            },
        ),
        migrations.CreateModel(
            name="EquipementImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="equipements/images/")),
                ("titre", models.CharField(blank=True, max_length=140)),
                (
                    "equipement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="images", to="assets.equipement"
                    ),
                ),
            ],
            options={
                "verbose_name": "Image d'equipement",
                "verbose_name_plural": "Images d'equipement",
            },
        ),
        migrations.CreateModel(
            name="EquipementFichier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fichier", models.FileField(upload_to="equipements/fichiers/")),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "equipement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="fichiers", to="assets.equipement"
                    ),
                ),
            ],
            options={
                "verbose_name": "Fichier d'equipement",
                "verbose_name_plural": "Fichiers d'equipement",
            },
        ),
    ]

from django.contrib import admin

from .models import AssetType, Equipement, EquipementFichier, EquipementImage


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    search_fields = ("nom",)
    list_display = ("nom",)


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "code_gmao",
        "status",
        "criticalite",
        "asset_type",
        "localisation",
        "fabricant",
        "modele",
        "teams_in_charge",
        "vendors",
        "cree_le",
    )
    list_filter = ("status", "criticalite", "asset_type", "localisation", "fabricant")
    search_fields = ("nom", "designation", "code_gmao", "numero_serie", "teams_in_charge", "vendors", "parts")
    autocomplete_fields = ("asset_type", "localisation", "fabricant", "modele", "parent")
    readonly_fields = ("cree_le", "modifie_le")


@admin.register(EquipementImage)
class EquipementImageAdmin(admin.ModelAdmin):
    list_display = ("equipement", "titre")
    search_fields = ("equipement__nom", "titre")
    autocomplete_fields = ("equipement",)


@admin.register(EquipementFichier)
class EquipementFichierAdmin(admin.ModelAdmin):
    list_display = ("equipement", "description")
    search_fields = ("equipement__nom", "description")
    autocomplete_fields = ("equipement",)

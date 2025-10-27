from rest_framework import serializers
from .models import Equipement

class EquipementSerializer(serializers.ModelSerializer):
    localisation_nom = serializers.CharField(source="localisation.nom", read_only=True)
    fabricant_nom = serializers.CharField(source="fabricant.nom", read_only=True)
    modele_nom = serializers.CharField(source="modele.nom", read_only=True)
    asset_type_nom = serializers.CharField(source="asset_type.nom", read_only=True)

    class Meta:
        model = Equipement
        fields = [
            "id", "nom", "designation", "code_gmao",
            "localisation", "localisation_nom",
            "criticalite", "status",
            "asset_type", "asset_type_nom",
            "fabricant", "fabricant_nom",
            "modele", "modele_nom",
            "numero_serie", "annee",
            "description",
            "teams_in_charge", "vendors", "parts",
            "parent",
            "cree_par", "cree_le", "modifie_le",
        ]
        read_only_fields = ("cree_par", "cree_le", "modifie_le")

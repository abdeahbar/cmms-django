from django import forms
from .models import Equipement

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = [
            "nom", "designation", "code_gmao",
            "localisation", "criticalite", "status",
            "asset_type", "fabricant", "modele",
            "numero_serie", "annee", "description",
            "parent",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "code_gmao": "Généré ou scanné (QR/Code-barres).",
            "parent": "Définir un parent pour créer un sous-actif.",
        }

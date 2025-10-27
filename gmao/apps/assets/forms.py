from django import forms
from django.forms import modelformset_factory

from .models import AssetType, Equipement, EquipementFichier, EquipementImage


class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = [
            "nom",
            "designation",
            "code_gmao",
            "localisation",
            "criticalite",
            "status",
            "asset_type",
            "fabricant",
            "modele",
            "numero_serie",
            "annee",
            "description",
            "teams_in_charge",
            "vendors",
            "parts",
            "parent",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "code_gmao": "Identifiant unique (QR ou code barre).",
            "parent": "Optionnel : selectionnez un parent pour creer un sous-actif.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        optional_fields = {
            "designation",
            "localisation",
            "asset_type",
            "fabricant",
            "modele",
            "numero_serie",
            "annee",
            "description",
            "teams_in_charge",
            "vendors",
            "parts",
            "parent",
        }

        labels = {
            "nom": "Name (Required)",
            "designation": "General",
            "code_gmao": "QR Code/Barcode",
            "localisation": "Location",
            "criticalite": "Criticality",
            "status": "Status",
            "asset_type": "Asset Types",
            "fabricant": "Manufacturer",
            "modele": "Model",
            "numero_serie": "Serial Number",
            "annee": "Year",
            "description": "Description",
            "teams_in_charge": "Teams in Charge",
            "vendors": "Vendors",
            "parts": "Parts",
            "parent": "Parent Asset",
        }

        placeholders = {
            "nom": "Enter Asset Name (Required)",
            "designation": "General notes about the asset",
            "code_gmao": "QR Code/Barcode",
            "description": "Add a description",
            "numero_serie": "Enter serial number",
            "annee": "Start typing",
            "teams_in_charge": "Start typing",
            "vendors": "Start typing",
            "parts": "Start typing",
        }

        select_like_fields = {"localisation", "asset_type", "fabricant", "modele", "parent"}

        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            if name in optional_fields:
                field.required = False
            label = labels.get(name)
            if label:
                field.label = label
            placeholder = placeholders.get(name)
            if placeholder:
                field.widget.attrs.setdefault("placeholder", placeholder)
            if name in select_like_fields:
                field.widget.attrs.setdefault("data-placeholder", "Start typing")

        self.fields["status"].widget = forms.Select(attrs={"class": "form-control"})
        self.fields["criticalite"].widget = forms.Select(attrs={"class": "form-control"})
        self.fields["annee"].widget.attrs.setdefault("inputmode", "numeric")

    def clean_annee(self):
        value = self.cleaned_data.get("annee")
        if value and not value.isdigit():
            raise forms.ValidationError("Utilisez uniquement des chiffres pour l'annee.")
        return value


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ["nom"]
        widgets = {"nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom du type"})}


class EquipementImageForm(forms.ModelForm):
    class Meta:
        model = EquipementImage
        fields = ("image", "titre")
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "titre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre optionnel"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


class EquipementFichierForm(forms.ModelForm):
    class Meta:
        model = EquipementFichier
        fields = ("fichier", "description")
        widgets = {
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Description optionnelle"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fichier"].required = False


EquipementImageFormSet = modelformset_factory(
    EquipementImage,
    form=EquipementImageForm,
    extra=3,
    can_delete=True,
)

EquipementFichierFormSet = modelformset_factory(
    EquipementFichier,
    form=EquipementFichierForm,
    extra=3,
    can_delete=True,
)

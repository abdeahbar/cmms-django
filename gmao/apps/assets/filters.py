import django_filters as df
from django.db.models import Q

from .models import Equipement


class EquipementFilter(df.FilterSet):
    q = df.CharFilter(method="search", label="Recherche")

    class Meta:
        model = Equipement
        fields = {
            "status": ["exact"],
            "criticalite": ["exact"],
            "localisation": ["exact"],
            "asset_type": ["exact"],
            "fabricant": ["exact"],
            "modele": ["exact"],
        }

    def search(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(
            Q(nom__icontains=value)
            | Q(designation__icontains=value)
            | Q(code_gmao__icontains=value)
            | Q(numero_serie__icontains=value)
        )

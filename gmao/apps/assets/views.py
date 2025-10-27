from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .filters import EquipementFilter
from .models import Equipement
from .serializers import EquipementSerializer


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EquipementFilter
    search_fields = ("nom", "designation", "code_gmao", "numero_serie")
    ordering_fields = ("nom", "cree_le", "criticalite", "status")
    ordering = ("nom",)

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    # Soft-delete: marque supprime_le, purge >30j si besoin
    def perform_destroy(self, instance):
        instance.supprime_le = now()
        instance.save(update_fields=["supprime_le"])

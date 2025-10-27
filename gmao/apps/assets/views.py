from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .filters import EquipementFilter
from .forms import EquipementFichierFormSet, EquipementForm, EquipementImageFormSet
from .models import Equipement, EquipementFichier, EquipementImage
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


class EquipementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Equipement
    form_class = EquipementForm
    template_name = "assets/equipement_form.html"
    success_url = reverse_lazy("users:admin-dashboard")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Acces refuse pour cette action.")
            return redirect("users:home")
        return super().handle_no_permission()

    def get_image_formset(self):
        if not hasattr(self, "_image_formset"):
            if self.request.method == "POST":
                self._image_formset = EquipementImageFormSet(
                    self.request.POST,
                    self.request.FILES,
                    prefix="images",
                    queryset=EquipementImage.objects.none(),
                )
            else:
                self._image_formset = EquipementImageFormSet(
                    prefix="images",
                    queryset=EquipementImage.objects.none(),
                )
        return self._image_formset

    def get_file_formset(self):
        if not hasattr(self, "_file_formset"):
            if self.request.method == "POST":
                self._file_formset = EquipementFichierFormSet(
                    self.request.POST,
                    self.request.FILES,
                    prefix="files",
                    queryset=EquipementFichier.objects.none(),
                )
            else:
                self._file_formset = EquipementFichierFormSet(
                    prefix="files",
                    queryset=EquipementFichier.objects.none(),
                )
        return self._file_formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("image_formset", self.get_image_formset())
        context.setdefault("file_formset", self.get_file_formset())
        return context

    def form_valid(self, form):
        image_formset = self.get_image_formset()
        file_formset = self.get_file_formset()

        if not (image_formset.is_valid() and file_formset.is_valid()):
            return self.form_invalid(form)

        form.instance.cree_par = self.request.user
        self.object = form.save()

        for image in image_formset.save(commit=False):
            if not image.image:
                continue
            image.equipement = self.object
            image.save()
        for image in image_formset.deleted_objects:
            image.delete()

        for fichier in file_formset.save(commit=False):
            if not fichier.fichier:
                continue
            fichier.equipement = self.object
            fichier.save()
        for fichier in file_formset.deleted_objects:
            fichier.delete()

        messages.success(self.request, "Equipement cree avec succes.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Merci de corriger les erreurs du formulaire.")
        return self.render_to_response(self.get_context_data(form=form))

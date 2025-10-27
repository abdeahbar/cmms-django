from django.urls import path

from .views import EquipementCreateView

app_name = "assets"

urlpatterns = [
    path("equipements/nouveau/", EquipementCreateView.as_view(), name="equipement-create"),
]

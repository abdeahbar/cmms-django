from django.db import models
from django.conf import settings
from django_fsm import FSMField
from apps.assets.models import Equipement

class OrdreTravail(models.Model):
    code = models.CharField(max_length=60, unique=True)
    equipement = models.ForeignKey(Equipement, on_delete=models.PROTECT, related_name="ordres")
    titre = models.CharField(max_length=200)
    etat = FSMField(default="brouillon")  # brouillon -> planifie -> en_cours -> termine -> clos
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.code

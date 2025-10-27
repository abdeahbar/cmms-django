from django.test import TestCase

from .filters import EquipementFilter
from .models import Equipement
from .views import EquipementViewSet


class EquipementFilterTests(TestCase):
    def setUp(self):
        self.matching = Equipement.objects.create(
            nom="Pompe principale",
            designation="Pompe de circulation",
            code_gmao="EQ-001",
            numero_serie="SN-1234",
        )
        Equipement.objects.create(
            nom="Ventilateur secondaire",
            designation="Ventilateur d'appoint",
            code_gmao="EQ-002",
            numero_serie="SN-9999",
        )

    def test_search_matches_multiple_fields(self):
        filt = EquipementFilter(data={"q": "pompe"}, queryset=Equipement.objects.all())
        results = list(filt.qs)

        self.assertEqual(results, [self.matching])

    def test_search_handles_empty_value(self):
        filt = EquipementFilter(data={"q": ""}, queryset=Equipement.objects.all())
        results = list(filt.qs.order_by("code_gmao"))

        self.assertEqual(len(results), 2)
        self.assertListEqual(results, list(Equipement.objects.order_by("code_gmao")))


class EquipementViewSetTests(TestCase):
    def test_perform_destroy_marks_supprime_le(self):
        equipement = Equipement.objects.create(
            nom="Compresseur",
            designation="Compresseur haute pression",
            code_gmao="EQ-100",
        )

        viewset = EquipementViewSet()
        self.assertIsNone(equipement.supprime_le)

        viewset.perform_destroy(equipement)
        equipement.refresh_from_db()

        self.assertIsNotNone(equipement.supprime_le)

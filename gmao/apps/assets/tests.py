from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import EquipementForm
from .filters import EquipementFilter
from .models import Equipement
from .views import EquipementViewSet

User = get_user_model()


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


class EquipementFormTests(TestCase):
    def test_form_validates_optional_fields(self):
        form = EquipementForm(
            data={
                "nom": "Pompe a eau",
                "code_gmao": "EQ-300",
                "status": "ONLINE",
                "criticalite": "NORMAL",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_non_numeric_year(self):
        form = EquipementForm(
            data={
                "nom": "Compresseur",
                "code_gmao": "EQ-301",
                "status": "ONLINE",
                "criticalite": "IMPORTANT",
                "annee": "20A4",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("annee", form.errors)


class EquipementCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="staff", password="StaffPass123", is_staff=True)

    def test_requires_authentication(self):
        response = self.client.get(reverse("assets:equipement-create"))
        self.assertEqual(response.status_code, 302)

    def test_creates_equipement_with_creator(self):
        self.client.login(username="staff", password="StaffPass123")
        payload = {
            "nom": "Generateur",
            "code_gmao": "EQ-999",
            "status": "OFFLINE",
            "criticalite": "CRITIQUE",
            "teams_in_charge": "Maintenance A",
            "vendors": "Vendor One",
            "parts": "Filter, Belt",
            "images-TOTAL_FORMS": "1",
            "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0",
            "images-MAX_NUM_FORMS": "1000",
            "images-0-id": "",
            "images-0-image": "",
            "images-0-titre": "",
            "images-0-DELETE": "",
            "files-TOTAL_FORMS": "1",
            "files-INITIAL_FORMS": "0",
            "files-MIN_NUM_FORMS": "0",
            "files-MAX_NUM_FORMS": "1000",
            "files-0-id": "",
            "files-0-fichier": "",
            "files-0-description": "",
            "files-0-DELETE": "",
        }
        response = self.client.post(reverse("assets:equipement-create"), payload, follow=True)
        self.assertEqual(response.status_code, 200)
        equipement = Equipement.objects.get(code_gmao="EQ-999")
        self.assertEqual(equipement.cree_par, self.user)
        self.assertEqual(equipement.teams_in_charge, "Maintenance A")
        self.assertEqual(equipement.vendors, "Vendor One")
        self.assertEqual(equipement.parts, "Filter, Belt")

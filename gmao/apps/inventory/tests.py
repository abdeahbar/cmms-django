from decimal import Decimal

from django.test import TestCase

from apps.assets.models import Equipement
from apps.core.models import Location

from .models import Part, PartType, PartVendor, Team, Vendor


class PartModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(nom="Magasin Central")
        self.asset = Equipement.objects.create(nom="Pompe", code_gmao="EQ-INV-1", status="ONLINE", criticalite="NORMAL")
        self.type_spare = PartType.objects.create(name="Spare")
        self.team = Team.objects.create(name="Maintenance A")
        self.vendor = Vendor.objects.create(name="Vendor One")

    def test_slug_generated_and_unique(self):
        part = Part.objects.create(name="Joint de pompe", location=self.location)
        self.assertTrue(part.slug)

        duplicate = Part.objects.create(name="Joint de pompe")
        self.assertNotEqual(part.slug, duplicate.slug)

    def test_relations_and_vendor_through_model(self):
        part = Part.objects.create(
            name="Filtre a huile",
            unit_cost=Decimal("12.50"),
            units_in_stock=5,
            minimum_in_stock=2,
        )
        part.types.add(self.type_spare)
        part.assets.add(self.asset)
        part.teams_in_charge.add(self.team)

        PartVendor.objects.create(
            part=part,
            vendor=self.vendor,
            reference="REF-123",
            lead_time_days=7,
            last_price=Decimal("11.75"),
            is_preferred=True,
        )

        self.assertIn(self.vendor, part.vendors.all())
        link = PartVendor.objects.get(part=part, vendor=self.vendor)
        self.assertEqual(link.lead_time_days, 7)
        self.assertTrue(link.is_preferred)

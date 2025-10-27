from __future__ import annotations

import uuid
from decimal import Decimal

from django.db import models
from django.utils.text import slugify


class PartType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Part(models.Model):
    class Unit(models.TextChoices):
        GENERAL = "GENERAL", "General"
        PCS = "PCS", "Pieces"
        M = "M", "Meters"
        L = "L", "Liters"
        KG = "KG", "Kilograms"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    name = models.CharField(max_length=120, db_index=True)
    description = models.TextField(blank=True, default="")
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    barcode = models.CharField(max_length=128, blank=True, default="", help_text="QR/Barcode text")
    part_number = models.CharField(max_length=64, blank=True, default="", help_text="Internal SKU")

    unit = models.CharField(max_length=16, choices=Unit.choices, default=Unit.GENERAL)
    units_in_stock = models.PositiveIntegerField(default=0)
    minimum_in_stock = models.PositiveIntegerField(default=1)

    types = models.ManyToManyField(PartType, blank=True, related_name="parts")
    location = models.ForeignKey(
        "core.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_parts",
    )
    assets = models.ManyToManyField("assets.Equipement", blank=True, related_name="inventory_parts")
    teams_in_charge = models.ManyToManyField(Team, blank=True, related_name="parts")
    vendors = models.ManyToManyField(Vendor, through="PartVendor", related_name="parts")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gmao_part"
        ordering = ("name",)
        indexes = [
            models.Index(fields=("name",)),
            models.Index(fields=("slug",)),
            models.Index(fields=("barcode",)),
            models.Index(fields=("part_number",)),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:100]
            slug = base_slug
            index = 1
            while Part.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                index += 1
                slug = f"{base_slug}-{index}"[:100]
            self.slug = slug
        super().save(*args, **kwargs)


    @property
    def is_low(self) -> bool:
        return self.units_in_stock <= self.minimum_in_stock

    def __str__(self) -> str:
        return self.name


class PartVendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="vendor_links")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="part_links")
    vendor_sku = models.CharField(max_length=64, blank=True, default="")
    last_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    lead_time_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("part", "vendor")
        ordering = ("vendor__name",)

    def __str__(self) -> str:
        return f"{self.vendor.name} - {self.part.name}"


class PartFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="parts/")
    label = models.CharField(max_length=120, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self) -> str:
        return self.label or self.file.name

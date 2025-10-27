from django.contrib import admin

from .models import Part, PartFile, PartType, PartVendor, Team, Vendor


@admin.register(PartType)
class PartTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class PartVendorInline(admin.TabularInline):
    model = PartVendor
    extra = 1
    autocomplete_fields = ("vendor",)


class PartFileInline(admin.TabularInline):
    model = PartFile
    extra = 1


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "units_in_stock", "minimum_in_stock", "is_low", "is_active", "updated_at")
    list_filter = ("unit", "is_active", "types")
    search_fields = ("name", "slug", "barcode", "part_number")
    autocomplete_fields = ("location", "assets", "types", "teams_in_charge")
    filter_horizontal = ("assets", "types", "teams_in_charge")
    inlines = (PartVendorInline, PartFileInline)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(PartVendor)
class PartVendorAdmin(admin.ModelAdmin):
    list_display = ("part", "vendor", "vendor_sku", "last_cost", "lead_time_days", "updated_at")
    search_fields = ("part__name", "vendor__name", "vendor_sku")
    autocomplete_fields = ("part", "vendor")


@admin.register(PartFile)
class PartFileAdmin(admin.ModelAdmin):
    list_display = ("part", "label", "uploaded_at")
    search_fields = ("part__name", "label")

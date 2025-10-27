from django.contrib import admin

from .models import AssetModel, Location, Manufacturer, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("code", "nom")
    search_fields = ("code", "nom")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ("nom",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ("nom",)


@admin.register(AssetModel)
class AssetModelAdmin(admin.ModelAdmin):
    list_display = ("nom", "fabricant")
    search_fields = ("nom", "fabricant__nom")
    autocomplete_fields = ("fabricant",)

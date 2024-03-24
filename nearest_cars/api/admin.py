from django.contrib import admin

from .models import Cargo, Location, Truck


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'pick_up_location', 'delivery_location', 'weight', 'description'
    )
    empty_value_display = '-пусто-'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'city', 'state', 'mail_zip', 'latitude', 'longitude'
    )
    empty_value_display = '-пусто-'


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = (
        'license_plate', 'current_location', 'load_capacity'
    )
    empty_value_display = '-пусто-'

from django.core.exceptions import ObjectDoesNotExist
from geopy import distance
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Cargo, Location, Truck


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'city',
            'state',
            'mail_zip',
            'latitude',
            'longitude'
        )
        model = Location


class PostCargoSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.CharField(write_only=True, max_length=5)
    delivery_location = serializers.CharField(write_only=True, max_length=5)

    class Meta:
        fields = (
            'pick_up_location',
            'delivery_location',
            'weight',
            'description'
        )
        model = Cargo
        validators = [
            UniqueTogetherValidator(
                queryset=Cargo.objects.all(),
                fields=('pick_up_location', 'delivery_location'),
                message='Место доставки не может совпадать '
                        'с местом подбора груза'
            ),
        ]

    def create(self, validated_data):
        pick_up_zip = validated_data.get('pick_up_location')
        delivery_zip = validated_data.get('delivery_location')

        try:
            pick_up_location = Location.objects.get(mail_zip=pick_up_zip)
            delivery_location = Location.objects.get(mail_zip=delivery_zip)

            cargo = Cargo.objects.create(
                pick_up_location=pick_up_location,
                delivery_location=delivery_location,
                weight=validated_data.get('weight'),
                description=validated_data.get('description')
            )
            return cargo
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Location with the specified zip code does not exist')

    def to_representation(self, instance):
        return CargoSerializer(instance).data


class CargoListSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    nearest_trucks = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'pick_up_location',
            'delivery_location',
            'weight',
            'description',
            'nearest_trucks'
        )
        model = Cargo
        validators = [
            UniqueTogetherValidator(
                queryset=Cargo.objects.all(),
                fields=('pick_up_location', 'delivery_location'),
                message='Место доставки не может совпадать '
                        'с местом подбора груза'
            ),
        ]

    def get_nearest_trucks(self, obj):
        pick_up_location = (
            obj.pick_up_location.latitude, obj.pick_up_location.longitude
        )
        trucks = Truck.objects.all()
        count_trucks = 0
        for truck in trucks:
            current_location = (
                truck.current_location.latitude,
                truck.current_location.longitude
            )
            if distance.distance(
                    pick_up_location, current_location).miles <= 450:
                count_trucks += 1
        return count_trucks


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    trucks = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'pick_up_location',
            'delivery_location',
            'weight',
            'description',
            'trucks'
        )
        model = Cargo
        validators = [
            UniqueTogetherValidator(
                queryset=Cargo.objects.all(),
                fields=('pick_up_location', 'delivery_location'),
                message='Место доставки не может совпадать '
                        'с местом подбора груза'
            ),
        ]

    def get_trucks(self, obj):
        pick_up_location = (
            obj.pick_up_location.latitude, obj.pick_up_location.longitude
        )
        trucks = Truck.objects.all()
        result = []
        for truck in trucks:
            current_location = (
                truck.current_location.latitude,
                truck.current_location.longitude
            )
            result.append({
                "license_plate": truck.license_plate,
                "distance": round(distance.distance(
                    pick_up_location, current_location).miles, ndigits=2)
            })
        return result


class TruckSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'license_plate',
            'current_location',
            'load_capacity'
        )
        model = Truck


class UpdateTruckSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField(write_only=True, max_length=5)

    class Meta:
        fields = (
            'current_location',
        )
        model = Truck

    def update(self, instance, validated_data):
        current_location_zip = validated_data.pop('current_location')
        try:
            location = Location.objects.get(mail_zip=current_location_zip)
            instance.current_location = location
            instance.save()
            return instance
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Location with the specified zip code does not exist')

    def to_representation(self, instance):
        return TruckSerializer(instance).data

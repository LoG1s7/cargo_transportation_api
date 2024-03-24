from rest_framework import viewsets

from .models import Cargo, Truck
from .serializers import (CargoListSerializer, CargoSerializer,
                          PostCargoSerializer, TruckSerializer,
                          UpdateTruckSerializer)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCargoSerializer
        if self.action == 'list':
            return CargoListSerializer
        return CargoSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateTruckSerializer
        return TruckSerializer

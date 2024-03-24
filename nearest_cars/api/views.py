from .serializers import (
    PostCargoSerializer,
    CargoListSerializer,
    CargoSerializer,
    TruckSerializer,
    UpdateTruckSerializer
)
from .models import Cargo, Truck

from rest_framework import viewsets


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCargoSerializer
        elif self.action == 'list':
            return CargoListSerializer
        return CargoSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateTruckSerializer
        return TruckSerializer

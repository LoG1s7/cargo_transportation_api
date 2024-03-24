from .views import CargoViewSet, TruckViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cargoes', CargoViewSet, basename='cargo')
router.register('trucks', TruckViewSet, basename='truck')

urlpatterns = [
    path('', include(router.urls)),
]

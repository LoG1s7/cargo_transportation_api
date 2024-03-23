from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Location(models.Model):
    city = models.CharField('Город')
    state = models.CharField('Штат')
    mail_zip = models.CharField(
        'Почтовый индекс', max_length=5
    )
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6)


class Cargo(models.Model):
    pick_up_location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Место подбора груза',
        related_name='cargo_pick_up'
    )
    delivery_location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Место доставки груза',
        related_name='cargo_delivery'
    )
    weight = models.PositiveSmallIntegerField(
        'Вес', validators=(MinValueValidator(1), MaxValueValidator(1000))
    )
    description = models.TextField('Описание')


class Truck(models.Model):
    license_plate = models.CharField(
        'Уникальный номер автомобиля', unique=True, max_length=5
    )
    current_location = models.ForeignKey(
        Location, on_delete=models.CASCADE,
        verbose_name='Текущая геопозиция',
        related_name='truck',

    )
    load_capacity = models.PositiveSmallIntegerField(
        'Грузоподъемность',
        validators=(MinValueValidator(1), MaxValueValidator(1000))
    )

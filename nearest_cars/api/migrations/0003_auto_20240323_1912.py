import csv
import random
from string import ascii_uppercase

from django.contrib.auth import settings
from django.db import migrations


def create_locations(apps, schema_editor):
    Location = apps.get_model('api', 'Location')
    with open(settings.LOCATIONS_DATA) as f:
        reader = csv.DictReader(f)
        locations = [
            Location(mail_zip=row['zip'],
                     latitude=row['lat'],
                     longitude=row['lng'],
                     city=row['city'],
                     state=row['state_name'],)
            for row in reader
        ]
        Location.objects.bulk_create(locations)


def generate_unique_number():
    number = random.randint(1000, 9999)
    letter = random.choice(ascii_uppercase)
    return f"{number}{letter}"


def create_trucks(apps, schema_editor):
    Truck = apps.get_model('api', 'Truck')
    Location = apps.get_model('api', 'Location')
    locations = list(Location.objects.all())
    for _ in range(20):
        truck = Truck.objects.create(
            license_plate=generate_unique_number(),
            current_location=random.choice(locations),
            load_capacity=random.randint(1, 1000)
        )
        truck.save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_alter_location_mail_zip'),
    ]

    operations = [
        migrations.RunPython(create_locations),
        migrations.RunPython(create_trucks),
    ]

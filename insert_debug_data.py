import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openfruit.settings")

from django.contrib.auth.models import User
from openfruit.geography.models import UserGeographySettings, Location, City


def main():
    print('Setting up Adin')
    admin = User(username='admin')
    admin.set_password('admin')
    admin.save()

    print('Setting up Geo Settings')
    settings = UserGeographySettings()
    settings.user = admin
    settings.location = Location.objects.get(generated_name='Covington, LA 70433')
    settings.save()


if __name__ == '__main__':
    main()



import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = get_user_model()

    User.objects.create_superuser(
        username='superuser@user.com',
        email='superuser@user.com',
        password='AdminStrongPass1!',
    )


def delete_superuser(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser)
    ]

from __future__ import unicode_literals
from django.db import models, migrations


def load_basisdaten_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "basisdaten_ddb1") #get json data

class Migration(migrations.Migration):

    dependencies = [
        ('basisdaten', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_basisdaten_from_fixture),
    ]


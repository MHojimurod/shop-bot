# Generated by Django 4.0.1 on 2022-01-28 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0010_diller_ball'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diller',
            old_name='ball',
            new_name='balls',
        ),
    ]

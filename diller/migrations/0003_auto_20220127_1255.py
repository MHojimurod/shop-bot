# Generated by Django 3.2.6 on 2022-01-27 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0002_busket_busket_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busket',
            name='count',
        ),
        migrations.RemoveField(
            model_name='busket',
            name='price',
        ),
    ]

# Generated by Django 4.0.1 on 2022-02-05 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0014_alter_ordergiftdiller_gift'),
        ('admin_panel', '0019_dillergifts_sellergifts'),
        ('seller', '0005_alter_ordergiftseller_gift'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Gifts',
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0008_busket_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busket',
            name='payment_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Naqd'), (1, 'Nasiya')], null=True),
        ),
    ]
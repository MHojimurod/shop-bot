# Generated by Django 4.0.1 on 2023-08-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0009_cashback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleseller',
            name='state',
            field=models.SmallIntegerField(default=0),
        ),
    ]

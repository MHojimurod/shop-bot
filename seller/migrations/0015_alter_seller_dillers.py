# Generated by Django 4.0.1 on 2022-10-01 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0022_alter_busket_payment_type_alter_busket_status'),
        ('seller', '0014_seller_dillers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='dillers',
            field=models.ManyToManyField(null=True, to='diller.Diller'),
        ),
    ]

# Generated by Django 4.0.1 on 2022-03-09 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0029_alter_baseproduct_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='serial_number',
            field=models.CharField(max_length=200),
        ),
    ]

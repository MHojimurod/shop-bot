# Generated by Django 4.0.1 on 2022-03-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0028_gifts_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='serial_number',
            field=models.TextField(),
        ),
    ]

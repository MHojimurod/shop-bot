# Generated by Django 4.0.1 on 2022-01-28 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_gifts'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='serial_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.1 on 2023-08-22 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_saleseller_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.saleseller'),
        ),
    ]

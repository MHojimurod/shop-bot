# Generated by Django 3.2.6 on 2022-01-27 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0004_auto_20220127_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busket',
            name='is_canceled',
        ),
        migrations.RemoveField(
            model_name='busket',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='busket',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='busket',
            name='is_purchased',
        ),
        migrations.AddField(
            model_name='busket',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

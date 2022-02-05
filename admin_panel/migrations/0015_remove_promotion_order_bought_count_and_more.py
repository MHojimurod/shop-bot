# Generated by Django 4.0.1 on 2022-02-04 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0014_promotion_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion_order',
            name='bought_count',
        ),
        migrations.AddField(
            model_name='promotion',
            name='bought_count',
            field=models.IntegerField(default=0),
        ),
    ]
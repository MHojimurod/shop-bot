# Generated by Django 4.0.1 on 2022-02-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0025_alter_promotion_bought_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion_order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Kutilmoqda'), (1, 'Qabul qilingan'), (2, 'Yuborilgan'), (3, 'Rad etilgan')], default=0),
        ),
    ]
# Generated by Django 4.0.1 on 2022-03-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0021_ordergiftdiller_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busket',
            name='payment_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Variant 1'), (1, 'Variant 2')], null=True),
        ),
        migrations.AlterField(
            model_name='busket',
            name='status',
            field=models.IntegerField(choices=[(0, 'Kutilmoqda'), (1, 'Qabul qilingan'), (2, 'Yuborilgan'), (3, 'Rad etilgan'), (4, 'Yetkazib berildi')], default=0),
        ),
    ]
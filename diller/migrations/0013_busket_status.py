# Generated by Django 4.0.1 on 2022-02-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0012_ordergiftdiller'),
    ]

    operations = [
        migrations.AddField(
            model_name='busket',
            name='status',
            field=models.IntegerField(choices=[(0, 'Kutinmoqda'), (1, 'Qabul qilingan'), (2, 'Yuborilgan'), (3, 'Rad etilgan')], default=0),
        ),
    ]

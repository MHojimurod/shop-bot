# Generated by Django 4.0.1 on 2022-02-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0026_promotion_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='diller_nasiya_ball',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

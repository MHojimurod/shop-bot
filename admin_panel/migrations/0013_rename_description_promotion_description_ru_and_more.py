# Generated by Django 4.0.1 on 2022-02-03 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0012_promotion_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='description',
            new_name='description_ru',
        ),
        migrations.AddField(
            model_name='promotion',
            name='description_uz',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

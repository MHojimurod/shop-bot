# Generated by Django 4.0.1 on 2022-02-02 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0009_delete_ordergift'),
        ('seller', '0002_seller_balls'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGiftSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.gifts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]
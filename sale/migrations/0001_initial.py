# Generated by Django 4.0.1 on 2023-08-17 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0037_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holder_name', models.CharField(max_length=200)),
                ('card_number', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaleSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField()),
                ('language', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.regions')),
            ],
        ),
    ]
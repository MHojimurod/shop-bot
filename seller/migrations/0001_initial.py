# Generated by Django 4.0.1 on 2022-01-29 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0006_ordergift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('shop', models.CharField(blank=True, max_length=300, null=True)),
                ('language', models.IntegerField(choices=[(0, 'uz'), (1, 'ru')])),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.district')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.regions')),
            ],
        ),
    ]

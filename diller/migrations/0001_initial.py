# Generated by Django 4.0.1 on 2022-01-26 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('language', models.IntegerField(choices=[(0, 'uz'), (1, 'ru')])),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.district')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.regions')),
            ],
        ),
    ]

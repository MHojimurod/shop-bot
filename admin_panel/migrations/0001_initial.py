# Generated by Django 4.0.1 on 2022-01-26 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uz_data', models.TextField()),
                ('ru_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('uz_data', models.TextField()),
                ('ru_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uz_data', models.TextField()),
                ('ru_data', models.TextField()),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.regions')),
            ],
        ),
    ]

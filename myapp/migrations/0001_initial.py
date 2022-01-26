# Generated by Django 3.2.6 on 2022-01-26 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField()),
                ('language', models.IntegerField(choices=[(0, 'uz'), (1, 'ru')])),
            ],
        ),
    ]
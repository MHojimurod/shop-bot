# Generated by Django 4.0.1 on 2023-08-22 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_card_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SerialNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('cashback', models.IntegerField()),
            ],
        ),
    ]

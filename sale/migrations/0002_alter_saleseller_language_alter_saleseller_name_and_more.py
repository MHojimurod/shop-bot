# Generated by Django 4.0.1 on 2023-08-19 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleseller',
            name='language',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='saleseller',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='saleseller',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

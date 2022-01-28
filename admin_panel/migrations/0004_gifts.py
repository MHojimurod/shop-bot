# Generated by Django 4.0.1 on 2022-01-28 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_product_ball'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=100)),
                ('name_ru', models.CharField(max_length=100)),
                ('ball', models.IntegerField()),
                ('image', models.ImageField(upload_to='gifts')),
            ],
        ),
    ]

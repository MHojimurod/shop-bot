# Generated by Django 4.0.1 on 2022-10-02 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0022_alter_busket_payment_type_alter_busket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diller',
            name='chat_id',
            field=models.IntegerField(default=0),
        ),
    ]
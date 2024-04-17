# Generated by Django 4.0.1 on 2024-03-28 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diller', '0024_alter_diller_language'),
        ('sale', '0013_alter_promocode_code_alter_promocode_seria_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocode',
            options={'ordering': ['car', 'letter', 'order']},
        ),
        migrations.AddField(
            model_name='promocode',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='promocode_images'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sale.saleseller'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='status',
            field=models.IntegerField(choices=[(1, 'Waiting'), (2, 'Not used'), (3, 'Used')], default=1),
        ),
        migrations.AddField(
            model_name='saleseller',
            name='last_promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sale.promocode'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promocodes', to='sale.car'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='diller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promocodes', to='diller.diller'),
        ),
        migrations.CreateModel(
            name='UserGift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gifts', to='sale.saleseller')),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='gift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promocodes', to='sale.usergift'),
        ),
    ]
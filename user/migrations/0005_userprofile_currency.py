# Generated by Django 2.0.7 on 2021-08-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0006_increase_name_max_length'),
        ('user', '0004_auto_20210812_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.Currency'),
        ),
    ]

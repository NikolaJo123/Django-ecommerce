# Generated by Django 2.0.7 on 2021-08-18 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_auto_20210812_2014'),
        ('user', '0007_auto_20210819_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavourites',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Variants'),
        ),
    ]

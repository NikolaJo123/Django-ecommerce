# Generated by Django 2.0.7 on 2021-08-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_userfavourites_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavourites',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]

# Generated by Django 2.0.7 on 2021-08-18 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_userfavourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavourites',
            name='product_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Product'),
        ),
    ]

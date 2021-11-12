# Generated by Django 2.0.7 on 2021-08-07 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_product_variant'),
        ('order', '0005_auto_20210725_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Variants'),
        ),
    ]
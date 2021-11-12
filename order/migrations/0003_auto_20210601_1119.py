# Generated by Django 2.0.7 on 2021-06-01 09:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210601_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='purchased_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
# Generated by Django 2.0.7 on 2021-05-01 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_messagealert'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagealert',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
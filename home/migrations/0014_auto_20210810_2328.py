# Generated by Django 2.0.7 on 2021-08-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_settinglang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='lang',
            field=models.CharField(max_length=6, null=True),
        ),
    ]

# Generated by Django 2.0.7 on 2021-08-11 14:47

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_product_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe'), ('mk', 'Македонски')], max_length=6)),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('detail', ckeditor_uploader.fields.RichTextUploadingField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
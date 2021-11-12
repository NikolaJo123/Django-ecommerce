# Generated by Django 2.0.7 on 2021-04-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210415_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=300)),
                ('country', models.CharField(max_length=300)),
                ('zipcode', models.CharField(max_length=300)),
                ('telephone', models.CharField(max_length=300)),
                ('message', models.TextField(max_length=600)),
                ('surname', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('New', 'New'), ('Read', 'Read'), ('Closed', 'Closed')], default='New', max_length=50)),
                ('ip', models.CharField(blank=True, max_length=50)),
                ('note', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='setting',
            name='email',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myflight',
            name='results',
            field=models.JSONField(null=True),
        ),
    ]

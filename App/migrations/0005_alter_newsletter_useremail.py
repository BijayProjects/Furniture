# Generated by Django 5.1.7 on 2025-04-03 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='userEmail',
            field=models.EmailField(max_length=254),
        ),
    ]

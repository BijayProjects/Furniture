# Generated by Django 5.1.7 on 2025-04-04 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]

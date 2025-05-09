# Generated by Django 5.1.7 on 2025-03-27 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('category_images', models.ImageField(upload_to='Category')),
            ],
        ),
    ]

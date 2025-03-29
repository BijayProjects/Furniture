from django.db import models

# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(unique=True,null=False)
    category_images = models.ImageField(upload_to='Category')

    def __str__(self):
        return self.category_title



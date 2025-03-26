from django.db import models

# Create your models here.

class Categories(models.Model):
    category_title = models.CharField(max_length=200)
    slug = models.SlugField()
    category_images = models.ImageField(upload_to='Category')
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_title
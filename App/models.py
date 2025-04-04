from django.db import models

# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(unique=True,null=False)
    category_images = models.ImageField(upload_to='Category')

    def __str__(self):
        return self.category_title

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    selling_price = models.PositiveIntegerField()
    descriptions = models.TextField()
    product_images = models.ImageField(upload_to='ProductImages')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name
    

class Newsletter(models.Model):
    userName = models.CharField(max_length=100)
    userEmail =models.EmailField(unique=False)
    submited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userName
    
class Comment(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    emailAddress = models.EmailField()
    Comments = models.TextField()
    Commented_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.firstName
    



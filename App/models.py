from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(unique=True,null=False)
    category_images = models.ImageField(upload_to='Category',help_text='Remove Image Background for better look.**')

    def __str__(self):
        return self.category_title

class About(models.Model):
    pass

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

class Blog(models.Model):
    blog_title = models.TextField()
    blog_descriptions = models.TextField()
    blog_images = models.ImageField(upload_to="Blogimages")
    post_at = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.blog_title

class BlogImage(models.Model):
    blog =models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='BlogImages')

    def __str__(self):
        return f"Image for {self.blog.blog_title}"    
    
class Comment(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    emailAddress = models.EmailField()
    Comments = models.TextField()
    Commented_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.firstName


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    product_name = models.CharField(max_length=200)
    product_images = models.ImageField(upload_to='OrderMedia')
    descriptions = models.TextField()
    selling_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price =models.PositiveIntegerField()

    #Customer 
    
    country = models.CharField(max_length=200)
    ordered_By = models.CharField(max_length=200)
    address = models.TextField()
    address2 = models.TextField(blank=True,null=True)
    state = models.TextField(blank=True, null=True)
    emailAddress = models.EmailField()
    phoneNumber = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    orderNote = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add= True, blank=False)
    is_read = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        creating = self.pk is None  
        old_status = None

        if not creating:
            old_status = Order.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if old_status != 'Completed' and self.status == 'Completed':
            PaidOrder.objects.create(
                ordered_By=self.ordered_By,
                address=self.address,
                phone_number = self.phoneNumber,
                product_name=self.product_name,
                product_images=self.product_images,
                status = self.status,
                quantity=self.quantity,
                total_price=self.total_price,
            )
        



class PaidOrder(models.Model):
    ordered_By = models.CharField(max_length=200)
    phone_number= models.IntegerField()
    address = models.TextField()
    product_name = models.CharField(max_length=200)
    product_images = models.ImageField(upload_to='OrderMedia')
    status = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    total_price =models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ordered_By


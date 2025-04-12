from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from datetime import timedelta
from django.utils import timezone

from .models import *

from django.core.mail import EmailMessage,send_mail

# Create your views here.

def Home(request):
    category_show = Category.objects.all()
    product = Product.objects.all()
    blog_show = Blog.objects.all().order_by('-id')
    
    context = {
        'category_show':category_show,
        'Products':product,
        'show_blog':blog_show,
    }
    return render(request, 'index.html',context)

def Shop(request):
    products = Product.objects.all().order_by('-id')
    context ={
        'product':products
    }
    return render(request, 'shop.html',context)


def NewsLetter(request):
    if request.method == 'POST':
        username = request.POST['user-name']
        useremail = request.POST['user-email']
        # if Newsletter.objects.filter(userEmail=useremail).exists():
        #     # messages(request,'This email address already exits!!')
        #     return HttpResponse('This email address already exit please try another!!')
        register_newsletter = Newsletter(userName= username,userEmail = useremail)
        email = EmailMessage(
            
            subject=f"Hi {username}, Get Notification of Your.PlaceFurniture",
            body='Your notify about our every news and blog of Product that might help you to what to choose for your Decoration.',
            to=[useremail])
        email.send()
        register_newsletter.save()
        return redirect('contact')
            
        


def SearchItems(request):
    
    if request.method == 'POST':
        search = request.POST.get('searched_items')
        match = Product.objects.filter(product_name__contains=search)

        context = {
            'get_items':match,
            "search":search,
            # 'cat_search':cat_search
        }
        return render(request,'searchItems.html', context)
    
    return render(request,'searchItems.html')


def ShowCategory(request,slug):
    showCat = Category.objects.get(slug=slug)

    context ={
        'show_category':showCat
    }
    return render(request, 'showCategory.html',context)

def About(request):
    return render(request, 'about.html')

def BlogPages(reqeust):
    showVlog = Blog.objects.all().order_by('-id')
    context = {
        "show_blog":showVlog
    }
    return render(reqeust, 'blog.html',context)

def ShowBlogs(request, id):
    view_detail_blog = get_object_or_404(Blog, id=id)
    now = timezone.now()
    time_diff = now - view_detail_blog.post_at
    minutes = time_diff.total_seconds() // 60
    
    if minutes <1:
        time_ago = "Just Now"
    elif minutes ==1:
        time_ago='1 minute ago'
    elif minutes < 60:
        time_ago = f"{int(minutes)} minutes ago"
    else:
        hours = minutes//60
        if hours == 1:
            time_ago = "1 hour ago"
        else:
            time_ago = f"{int(hours)} hours ago"
    
    context ={
        'vdb':view_detail_blog,
        'time_ago':time_ago
    }
    
    return render(request, 'showBlog.html',context)

def Contact(request):
    if request.method == "POST":
        firstname = request.POST['first-name']
        lastname = request.POST['last-name']
        emailaddress = request.POST['email-address']
        client_message = request.POST['client-message']
        
        Client_contact = Comment(firstName = firstname, lastName= lastname, emailAddress=emailaddress,Comments =client_message)
        Client_contact.save()
        messages.info(request, f'Hi {firstname} Thank you for reaching out to us. We hope you have a wonderful shopping experience!')
        return redirect('contact')

    return render(request, 'contact.html')


def OrderDetail(request,slug):
    selected_product = Product.objects.get(slug=slug)
    context = {
        'show_details':selected_product
    }
    return render(request, 'OrderDetail.html',context)

def CheckOut(request,slug):

    if request.method == "POST":
        checkouts = Product.objects.get(slug=slug)
        productName = checkouts.product_name
        productImages = checkouts.product_images
        description = checkouts.descriptions
        sellingPrice = checkouts.selling_price
        quantity = request.POST['quantitys']
        totalPrices = request.POST['total_price']
        country = request.POST['country']
        c_firstName = request.POST['firstName']
        c_lastName = request.POST['lastName']
        c_Address = request.POST['c_address']
        address2 = request.POST.get("optionalAddress", '')
        state = request.POST.get('c_state_country','')
        email_address = request.POST['email']
        phone_number = request.POST['phoneNumber']
        orderNotes = request.POST.get('orderNote','')

        reg_orders = Order(product_name=productName,product_images = productImages,descriptions=description,selling_price=sellingPrice,quantity=quantity,
        total_price=totalPrices,country=country,ordered_By=f'{c_firstName} {c_lastName}', address = c_Address, address2=address2,state =state,emailAddress=email_address,phoneNumber=phone_number,orderNote=orderNotes)
        reg_orders.save()

        return redirect('successfull')




    checkouts = Product.objects.get(slug=slug)
    context = {
        'checkOrders':checkouts
    }
    return render(request,'checkout.html',context)

def Successfull(request):
    return render(request, 'thankyou.html')
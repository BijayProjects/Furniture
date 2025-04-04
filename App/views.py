from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import *

from django.core.mail import EmailMessage,send_mail

# Create your views here.

def Home(request):
    category_show = Category.objects.all()
    product = Product.objects.all()
    context = {
        'category_show':category_show,
        'Products':product
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

def Blog(reqeust):
    return render(reqeust, 'blog.html')

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


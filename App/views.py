from django.shortcuts import render

from .models import Category


# Create your views here.

def Home(request):
    category_show = Category.objects.all()
    context = {
        'category_show':category_show,
    }
    return render(request, 'index.html',context)
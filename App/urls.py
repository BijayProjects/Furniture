from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home , name='home'),
    path('Shop/',views.Shop, name='shop'),
    path('Search-Items/',views.SearchItems, name='productsearch'),
    path('showcategory/<slug:slug>',views.ShowCategory, name='showcategory'),
    path('about/',views.About, name='about'),
    path('Blog/',views.Blog, name='blog'),
    path('Contact/',views.Contact, name='contact'),
    path('newsletter/',views.NewsLetter, name='newsletter'),
]
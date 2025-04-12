from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home , name='home'),
    path('Shop/',views.Shop, name='shop'),
    path('Search-Items/',views.SearchItems, name='productsearch'),
    path('showcategory/<slug:slug>',views.ShowCategory, name='showcategory'),
    path('about/',views.About, name='about'),
    path('Blog/',views.BlogPages, name='blog'),
    path('showBlogs/<int:id>',views.ShowBlogs, name='showblog'),
    path('Contact/',views.Contact, name='contact'),
    path('newsletter/',views.NewsLetter, name='newsletter'),
    path('orderdetail/<slug:slug>',views.OrderDetail, name='orderdetail'),
    path('checkout/<slug:slug>',views.CheckOut,name='checkout'),
    path('OrderSuccessfull/',views.Successfull, name='successfull'),

]
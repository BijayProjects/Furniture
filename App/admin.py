from django.contrib import admin
from .models import Category,Product,Newsletter,Comment,Order,PaidOrder,Blog,BlogImage
from django.urls import reverse

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from django.http import JsonResponse

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.urls import path

import pandas as pd

# Register your models here.

# Category Download

def export_categories_as_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="categories.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Exported Categories")  # Title
    y_position = height - 80  

    # Table Data (Header Row)
    data = ["Category Title", "Slug"]

    # Add Category Data
    for category in queryset:
        data.append([category.category_title, category.slug])

    # Create Table
    table = Table(data, colWidths=[50, 200, 200])
    
    # Style the Table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all columns
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.setStyle(style)

    # Draw Table
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, y_position - (len(data) * 20))  # Adjust y-position dynamically

    p.showPage()
    p.save()

    return response

export_categories_as_pdf.short_description = "Export selected categories to PDF"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_title','slug','images_tag','Action']
    list_filter = ('category_title',)
    list_display_links=['category_title']

    actions = [export_categories_as_pdf]



    # Display the Images Logic
    def images_tag(self,obj):
        if obj.category_images:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.category_images.url))

        return "(No Image Found)"
    
    images_tag.short_description = 'Cat Image'

    def Action(self, obj):
        url = reverse("admin:App_category_change", args=[obj.id])
        return format_html('<a class="edit-button" href="{}">Edit</a>',url)

    Action.short_description = "Action"
    

    class Media:
        css = {
            "all": ("css/custom.css",)
        }



    

def Product_Pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Product_Data.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Exported Products")  # Title
    y_position = height - 80  

    
    data = [["Product Name", "Slug", "Category", "Selling Price", "Descriptions", "Created At"]]

   
    for product in queryset:
        data.append([
            product.id,
            product.product_name,
            product.slug,
            str(product.category),  # Ensure category is a string
            product.selling_price,
            (product.descriptions[:50] + "...") if product.descriptions else "",  # Shorten descriptions
            product.created_at.strftime("%Y-%m-%d"),  # Format date
        ])

  
    table = Table(data, colWidths=[50, 150, 100, 100, 80, 200, 100])

    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all columns
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.setStyle(style)

   
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, y_position - (len(data) * 20))  # Adjust Y-position

    p.showPage()
    p.save()

    return response

Product_Pdf.short_description = "Export selected products to PDF"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['product_name','slug','category', 'selling_price','description_wrapped','images_view','created_at']
    actions = [Product_Pdf]
    list_display_links= ['product_name']

    def images_view(self, obj):
        if obj.product_images:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.product_images.url))

        return "(No Image Found)"
    
    images_view.short_description = 'Cat Image'

    def description_wrapped(self, obj):
        return obj.descriptions[:50] + "..." if len(obj.descriptions) > 25 else obj.descriptions
    description_wrapped.short_description = "Description"


@admin.register(Newsletter)

class NewsleterAdmin(admin.ModelAdmin):
    list_display=['userName','userEmail','submited_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['firstName','lastName','emailAddress','Comments','Commented_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_name','Images','descriptions','selling_price','quantity','total_price','country','ordered_By','address','address2','state','emailAddress','phoneNumber','status','orderNote','order_date']
    list_display_links=('product_name',)
    list_filter = ['product_name']
    list_editable = ['status']

    def Images(self, obj):
        if obj.product_images:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.product_images.url))

        return "(No Image Found)"
    
    Images.short_description = 'Cat Image'


def notification_count(request):
    count = Order.objects.filter(is_read=False).count()
    return JsonResponse({'count': count})

# admin.site.get_urls = lambda: [
#     path('notification-count/', admin.site.admin_view(notification_count), name='notification_count'),
# ] + admin.site.get_urls()

original_get_urls = admin.site.get_urls

def get_urls():
    urls =original_get_urls()
    custome_urls = [
        path('notification-count/', admin.site.admin_view(notification_count), name='notification_count'),
    ]
    return custome_urls + urls


# sells Invoice Download for paid products
def SellsInvoice(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Product_Data.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Sells Invoice")  # Title
    y_position = height - 80  

    
    data = [['ordered_By','address','product_name','quantity','total_price','completed_at']]

   
    for product in queryset:
        data.append([
            product.ordered_By,
            str(product.address),  # Ensure category is a string
            product.product_name,
            product.quantity,
            product.total_price,
            #  [:50] + "...") if product.descriptions else "",  # Shorten descriptions
            product.completed_at.strftime("%Y-%m-%d"),  # Format date
        ])

  
    table = Table(data, colWidths=[50, 150, 100, 100, 80, 200, 100])

    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all columns
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.setStyle(style)

   
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, y_position - (len(data) * 20))  # Adjust Y-position

    p.showPage()
    p.save()

    return response

Product_Pdf.short_description = "Export selected products to PDF"

@admin.register(PaidOrder)
class AdminPaidOrder(admin.ModelAdmin):
    list_display =['ordered_By','address','product_name','ProductImages','quantity','total_price','completed_at']
    actions = [SellsInvoice]
    list_filter = ['ordered_By']
    # def Images(self, obj):
    #     if obj.product_images:
    #         return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.product_images.url))

    #     return "(No Image Found)"
    
    def ProductImages(self, obj):
        if obj.product_images:
            return format_html(' <img src="{}" width="100" height="100" style="border-radius:10px;"/>'.format(obj.product_images.url))
        return "(No Images Avaiable)"
    ProductImages.short_description = 'Images'


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines =[BlogImageInline]

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    pass
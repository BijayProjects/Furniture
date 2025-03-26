from django.contrib import admin


# export model for excels
from django.http import HttpResponse
import pandas as pd
from django.utils.timezone import make_naive
from django.utils.html import format_html
from django.utils.timezone import now
from datetime import timedelta
from django.forms import Textarea


# Register your models here.
# @admin.register(Categories)
# class admincategory(admin.ModelAdmin):
#     list_display=['id','category_title','slug','images_tag']
#     list_display_links =['category_title']

#     def images_tag(self,obj):
#         if obj.category_images:
#             return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.category_images.url))

#         return "(No Image Found)"
#     images_tag.short_description = 'Cat Image'




# def Export_to_Excel(modeladmin, request,queryset):
#     """"
#         Custom admin action to export selected objects to an excel file.
#     """

#     # convert queryset to dataFrame
#     data = list(queryset.values('id','poduct_name','slug','selling_price','product_images', 'descriptions','category','quantity' ,'created_at'))

#     for item in data:
#         if item['created_at']:
#             item['created_at'] = make_naive(item['created_at'])

#     df =pd.DataFrame(data)

#     # Create excel response
#     response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     response["Content-Disposition"] = 'attachment; filename="products.xlsx"'

#     with pd.ExcelWriter(response, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False, sheet_name="Products")

#     return response

# Export_to_Excel.short_description = "Download Excel"  # Button label in Django admin




# @admin.register(Product)
# class AdminProduct(admin.ModelAdmin):
#     search_fields=('product_name','slug')
#     list_filter=('category','created_at')
#     actions= [Export_to_Excel]

#     list_display = ['id','product_name','slug','selling_price','image_tag', 'description_wrapped','category','quantity' ,'created_at','time_since_added']
#     list_display_links = ['product_name']

#     formfield_overrides={
#         models.TextField:{'widget': Textarea(attrs={'rows':5, 'cols':50}) }
#     }
#     def description_wrapped(self, obj):
#         return obj.descriptions[:25] + "..." if len(obj.descriptions) > 25 else obj.descriptions
#     description_wrapped.short_description = "Description"

#     def image_tag(self,obj):
#         if obj.product_images:
#             return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.product_images.url))

#         return "(No Image Found)"
#     image_tag.short_description = 'Product Image'

#     def time_since_added(self, obj):
#         time_diff = now() - obj.created_at
#         if time_diff < timedelta(minutes=1):
#             return "Just now"
#         elif time_diff < timedelta(hours=1):
#             return f"{int(time_diff.total_seconds() // 60)} minutes ago"
#         elif time_diff < timedelta(days=1):
#             return f"{int(time_diff.total_seconds() // 3600)} hours ago"
#         else:
#             return f"{time_diff.days} days ago"

#     time_since_added.short_description = "Added"  # Column name in Admin


# @admin.register(Order)
# class AdminOrder(admin.ModelAdmin):
#     list_display = ['id','firstName',
#                     'lastName',
#                     'emailAddress',
#                     'phoneNumber',
#                     'country',
#                     'address',
#                     'optionalAddress',
#                     'stateCountry',
#                     'orderNote',
#                     'productName',
#                     'quantity',
#                     'productImages',
#                     'total',
#                     'Descriptions'
#                     ]
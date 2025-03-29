from django.contrib import admin
from .models import Category
from django.urls import reverse

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Register your models here.

# Category Download

def export_as_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exported_data.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y_position = height - 40  # Start near the top of the page
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, "Exported Data")
    
    p.setFont("Helvetica", 12)
    y_position -= 30  # Move down

    for obj in queryset:
        p.drawString(100, y_position, f"{obj.id} - {obj.name}")  # Modify fields accordingly
        y_position -= 20  # Move to the next line

        if y_position < 50:  # Create a new page if needed
            p.showPage()
            y_position = height - 40

    p.showPage()
    p.save()

    return response

export_as_pdf.short_description = "Export selected to PDF"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_title','slug','images_tag','Action']
    list_filter = ('category_title',)
    list_display_links=['category_title']



    # Display the Images Logic
    def images_tag(self,obj):
        if obj.category_images:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/> '.format(obj.category_images.url))

        return "(No Image Found)"
    
    images_tag.short_description = 'Cat Image'

    def Action(self, obj):
        url = reverse("admin:App_category_change", args=[obj.id])
        return format_html('<a class="button" href="{}">Edit</a>',url)

    Action.short_description = "Action"


    class Media:
        css = {
            "all": ("App/static/css/custom.css",),
        }



    

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
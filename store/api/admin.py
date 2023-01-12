from django.contrib import admin

from api.models import Product

admin.site.site_header = "Store Administration"
admin.site.site_title = "Store Administration"
admin.site.register(Product)

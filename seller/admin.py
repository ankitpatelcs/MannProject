from atexit import register
from django.contrib import admin

from seller.models import Product, Seller

# Register your models here.
admin.site.register(Seller)
#admin.site.register(Product)

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display=['name','des','price','quantity','discount','seller','pic']

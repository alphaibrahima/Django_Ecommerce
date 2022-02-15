from django.contrib import admin
from .models import Product



# @admin.register()
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'price', 'stock', 'category', 'created_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    list_editable = ('price', 'stock')
    list_filter = ('category', 'created_date', 'price', 'modified_date', 'stock')
    search_fields = ['product_name', 'category', 'price', 'description']
    ordering = ('price', 'created_date')
    




admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from .models import Category, Product, Attribute, AttributeValue, ProductVariant

class ProductVariantInline(admin.TabularInline):
    model=ProductVariant
    extra=1
    filter_horizontal = ("attribute_values", )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "base_price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name", )}
    inlines = [ProductVariantInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    prepopulated_fields = {"slug": ("name", )}

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value")


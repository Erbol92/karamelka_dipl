from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.


class ProductIngredientsInline(admin.TabularInline):
    model = ProductIngredients
    extra = 1


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]
    inlines = [
        ProductIngredientsInline,
    ]

    def preview(self, obj):
        return mark_safe(f'<img style="width:96px" src="{obj.image.url}">')


class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_category',)}


admin.site.register(Ingridients)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Cart)
admin.site.register(Bisquit)

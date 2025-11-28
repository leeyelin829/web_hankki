from django.contrib import admin
from .models import HealthCategory, LunchboxModel


@admin.register(HealthCategory)
class HealthCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(LunchboxModel)
class LunchboxModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'food_category', 'price', 'discount_price', 'stock', 'supplier', 'created')
    list_filter = ('food_category', 'health_category', 'supplier')
    search_fields = ('name', 'description')
    readonly_fields = ('created', 'updated')

    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'description', 'food_category', 'health_category')
        }),
        ('가격 정보', {
            'fields': ('price', 'discount_price')
        }),
        ('공급 정보', {
            'fields': ('supplier', 'stock')
        }),
        ('시간 정보', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
from django.contrib import admin

import items.models as models

admin.site.site_header = 'Товары'
admin.site.site_title = 'Товары'

@admin.register(models.CurrencyUSDRate)
class CurrencyUSDRate(admin.ModelAdmin):
    list_display = ('name', 'rate')
    list_display_links = ('name',)
    ordering = ('name',)
    list_editable = ('rate',)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'currency')
    list_display_links = ('title',)
    search_fields = ('title', 'description',)
    ordering = ('title', 'description',)
    list_editable = ('price', 'currency')

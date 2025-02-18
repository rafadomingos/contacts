from django.contrib import admin
from contact import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'show', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'description')
    list_filter = ('created_at',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('first_name', 'last_name', 'show')
    list_display_links = 'id', 'phone',
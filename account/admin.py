from django.contrib import admin
from .models import Profile, Client, Visit, Inventory, Order


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']


class ClientList(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'zip', 'phone')
    list_filter = ('first_name', 'last_name', 'phone')
    search_fields = ('first_name', 'last_name', 'phone')
    ordering = ['first_name']


class VisitList(admin.ModelAdmin):
    list_display = ('visit_note', 'date', 'client', 'helped_by')
    list_filter = ('date', 'client')
    search_fields = ('date', 'client')
    ordering = ('date', 'client')


class InventoryList(admin.ModelAdmin):
    list_display = ('UPScode', 'item_description')
    list_filter = ('UPScode', 'item_description')
    search_fields = ('UPScode', 'item_description')
    ordering = ('UPScode', 'item_description')


class OrderList(admin.ModelAdmin):
    list_display = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity', 'date')
    list_filter = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity', 'date')
    search_fields = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity', 'date')
    ordering = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity', 'date')


admin.site.register(Client)
admin.site.register(Visit)
admin.site.register(Inventory)
admin.site.register(Order)

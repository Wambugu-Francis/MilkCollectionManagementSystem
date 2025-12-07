from django.contrib import admin
from .models import Farmer, MilkCollection

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['farmer_id', 'first_name', 'last_name', 'phone_number', 'location', 'is_active', 'date_registered']
    list_filter = ['is_active', 'date_registered', 'location']
    search_fields = ['farmer_id', 'first_name', 'last_name', 'phone_number', 'id_number']
    readonly_fields = ['farmer_id', 'date_registered']

@admin.register(MilkCollection)
class MilkCollectionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'quantity', 'collection_date', 'total_amount', 'sms_sent']
    list_filter = ['collection_date', 'sms_sent']
    search_fields = ['farmer__farmer_id', 'farmer__first_name', 'farmer__last_name']
    readonly_fields = ['total_amount', 'created_at']

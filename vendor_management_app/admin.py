from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance

# Registering models
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)

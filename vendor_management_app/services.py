from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Count, Avg, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.http import JsonResponse
from vendor_management_app.models import HistoricalPerformance, PurchaseOrder, Vendor
from vendor_management_app.serializers import HistoricalPerformanceSerializer, PurchaseOrderSerializer, VendorSerializer

def update_vendor_metrics(vendor):
    # On-Time Delivery Rate
    completed_purchases = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_purchases.filter(delivery_date__lte=F('acknowledgment_date'))
    on_time_delivery_rate = on_time_deliveries.count() / completed_purchases.count() if completed_purchases.count() > 0 else 0
    vendor.on_time_delivery_rate = on_time_delivery_rate

    # Quality Rating Average
    quality_rating_avg = completed_purchases.filter(quality_rating__isnull=False).aggregate(average=Avg('quality_rating'))['average']
    vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg is not None else 0.0

    # Average Response Time
    response_times = completed_purchases.filter(acknowledgment_date__isnull=False).annotate(
        response_time=Coalesce('acknowledgment_date', F('issue_date')) - F('issue_date')
    )
    avg_response_time = response_times.aggregate(average=Avg('response_time'))['average']
    vendor.average_response_time = avg_response_time.total_seconds() if avg_response_time is not None else 0.0

    # Fulfilment Rate
    fulfilled_purchases = completed_purchases.exclude(quality_rating__lt=3)  # Example condition for successful fulfilment
    fulfilment_rate = fulfilled_purchases.count() / completed_purchases.count() if completed_purchases.count() > 0 else 0
    vendor.fulfilment_rate = fulfilment_rate

    vendor.save()
    
# Create a new vendor
def create_vendor(request):
    data = request.data
    vendor = Vendor.objects.create(
        name = data['name'],
        contact_details = data['contact_details'],
        address = data['address'],
        vendor_code = data['vendor_code'],
        on_time_delivery_rate = data['on_time_delivery_rate'],
        quality_rating_avg = data['quality_rating_avg'],
        average_response_time = data['average_response_time'],
        fulfilment_rate = data['fulfilment_rate']
    )
    update_vendor_metrics(vendor)
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)

#  List all vendors
def get_vendor_list(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)    

# Retrieve a specific vendor's details
def get_vendor_detail(request, pk):    
    vendor = Vendor.objects.get(id=pk)
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)

# Update a vendor's details
def update_vendor(request, pk):
    data = request.data
    vendor = Vendor.objects.get(id=pk)
    serializer = VendorSerializer(instance=vendor, data=data)
    if serializer.is_valid():
        serializer.save()
        update_vendor_metrics(vendor)
    return Response(serializer.data)

# Delete a vendor
def delete_vendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    vendor.delete()
    return Response('Vendor is deleted !')

# Create a purchase order
def create_purchase_order(request):
    data = request.data
    vendor_data = data.get('vendor', {})    
    vendor_instance, created = Vendor.objects.get_or_create(id=vendor_data.get('id'), defaults=vendor_data)
    purchase_order = PurchaseOrder.objects.create(
        po_number = data['po_number'],
        vendor = vendor_instance,
        order_date = data['order_date'],
        delivery_date = data['delivery_date'],
        items = data['items'],
        quantity = data['quantity'],
        status = data['status'],
        quality_rating = data['quality_rating'],
        issue_date = data['issue_date'],
        acknowledgment_date = data['acknowledgment_date']
    )
    update_vendor_metrics(vendor_instance)
    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)

# List all purchase orders with an option to filter by vendor.
def get_purchase_orders_list(request):
    vendor_id = request.query_params.get('vendor_id', None)    
    if vendor_id is not None:
        purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    else:        
        purchase_orders = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data)    

# Retrieve details of a specific purchase order
def get_purchase_order_detail(request, pk):        
    purchase_order = PurchaseOrder.objects.get(id=pk)
    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)

# Update a purchase order
def update_purchase_order(request, pk):
    data = request.data
    purchase_orders = PurchaseOrder.objects.get(id=pk)
    serializer = PurchaseOrderSerializer(instance=purchase_orders, data=data)
    if serializer.is_valid():
        serializer.save()
        update_vendor_metrics(purchase_orders.vendor)
    return Response(serializer.data)

# Delete a purchase order
def delete_purchase_order(request, pk):
    purchase_order = PurchaseOrder.objects.get(id=pk)
    purchase_order.delete()
    return Response('Purchase Order is deleted !')

# Retrieve a vendor's performance metrics
def get_historical_performance_detail(request, pk):    
    historical_performance = HistoricalPerformance.objects.filter(vendor__id=pk)
    serializer = HistoricalPerformanceSerializer(historical_performance, many=True)
    return Response(serializer.data)

# Vendor's acknowledgement
# def acknowledge_purchase_order_services(request, pk):
def acknowledge_purchase_order_services(pk, request=None):
    try:
        purchase_order = PurchaseOrder.objects.get(id=pk)
        if purchase_order.acknowledgment_date:
            return JsonResponse({'message': 'Purchase order already acknowledged.'}, status=400)        
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()        
        update_vendor_metrics(purchase_order.vendor)
        return JsonResponse({'message': 'Purchase order acknowledged successfully.'}, status=200)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'message': 'Purchase order not found.'}, status=404)

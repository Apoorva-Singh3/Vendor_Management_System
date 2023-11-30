from django.test import TestCase
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .services import (
    update_vendor_metrics,
    create_vendor,
    create_purchase_order,
    acknowledge_purchase_order_services,
    get_vendor_list,
    get_vendor_detail,
    update_vendor,
    delete_vendor,
    get_purchase_orders_list,
    get_purchase_order_detail,
    update_purchase_order,
    delete_purchase_order,
    get_historical_performance_detail,
)

class ServicesTestCase(TestCase):
    def test_create_vendor(self):        
        data = {
            'name': 'Test Vendor',
            'contact_details': 'Contact',
            'address': 'Address',
            'vendor_code': 'V1',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 10.5,
            'fulfilment_rate': 0.9,
        }
        
        request = type('Request', (object,), {'data': data})

        response = create_vendor(request)
        self.assertEqual(response.status_code, 200)
        
        vendor = Vendor.objects.get(name='Test Vendor')
        self.assertEqual(vendor.on_time_delivery_rate, 0.0)
    
    def test_create_purchase_order(self):        
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")

        data = {
            'po_number': 'PO123',
            'vendor': {'id': vendor.id},
            'order_date': timezone.now(),
            'delivery_date': timezone.now(),
            'items': {},
            'quantity': 1,
            'status': 'completed',
            'quality_rating': 4,
            'issue_date': timezone.now(),
            'acknowledgment_date': timezone.now(),
        }
        
        request = type('Request', (object,), {'data': data})

        response = create_purchase_order(request)
        self.assertEqual(response.status_code, 200)

        purchase_order = PurchaseOrder.objects.get(po_number='PO123')
        self.assertEqual(purchase_order.vendor.on_time_delivery_rate, 1.0)

    def test_acknowledge_purchase_order_services(self):        
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")

        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={},
            quantity=1,
            status='completed',
            quality_rating=4,
            issue_date=timezone.now(),
        )

        response = acknowledge_purchase_order_services(purchase_order.id)
        self.assertEqual(response.status_code, 200)
        
        purchase_order.refresh_from_db()
        self.assertIsNotNone(purchase_order.acknowledgment_date)
        
    def test_get_vendor_list(self):
            
        Vendor.objects.create(
            name="Vendor1", 
            contact_details="Contact1", 
            address="Address1", 
            vendor_code="V1",
            on_time_delivery_rate= 0.0,
            quality_rating_avg=5.6,
            average_response_time=11.8,
            fulfilment_rate=4.8,
            )
        Vendor.objects.create(
            name="Vendor2", 
            contact_details="Contact2", 
            address="Address2",
            vendor_code="V2",
            on_time_delivery_rate= 0.0,
            quality_rating_avg=5.6,
            average_response_time=11.8,
            fulfilment_rate=4.8,
            )

        request = type('Request', (object,), {})
        response = get_vendor_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  

    def test_get_vendor_detail(self):
            
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")

        request = type('Request', (object,), {})
        response = get_vendor_detail(request, vendor.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        vendor = Vendor.objects.create(
            name="John Doe",
            contact_details="4561348960",
            address="Hudson Street, New York",
            vendor_code="JDN",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfilment_rate=0.0
        )

        data = {
            "id": vendor.id,
            "name": "Peter Parker",
            "contact_details": "3245678901",
            "address": "Hudson Drive, Las Vegas",
            "vendor_code": "PPL",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 0.0,
            "average_response_time": 0.0,
            "fulfilment_rate": 0.0
        }

        request = type('Request', (object,), {'data': data})
        response = update_vendor(request, vendor.id)
        self.assertEqual(response.status_code, 200)

        vendor.refresh_from_db()
        self.assertEqual(vendor.name, 'Peter Parker')  
        self.assertEqual(vendor.vendor_code, 'PPL')  


    def test_delete_vendor(self):
            
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")

        request = type('Request', (object,), {})
        response = delete_vendor(request, vendor.id)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(id=vendor.id)
        
    def test_get_purchase_orders_list(self):
            
        vendor1 = Vendor.objects.create(
            name="Vendor1", 
            contact_details="Contact1", 
            address="Address1", 
            vendor_code="V1",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfilment_rate=0.0,
        )
        vendor2 = Vendor.objects.create(
            name="Vendor2", 
            contact_details="Contact2", 
            address="Address2", 
            vendor_code="V2",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfilment_rate=0.0,
        )

        PurchaseOrder.objects.create(
            po_number='PO1', 
            vendor=vendor1,             
            order_date=timezone.now(), 
            delivery_date=timezone.now(), 
            items={'item1': 'description1'},  
            quantity=1,
            status='completed',          
            quality_rating=4,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )
        
        PurchaseOrder.objects.create(
            po_number='PO2',
            vendor=vendor2,             
            order_date=timezone.now(), 
            delivery_date=timezone.now(), 
            items={'item2': 'description2'},  
            quantity=1,
            status='completed',          
            quality_rating=4,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )            
        
        request_without_filter = type('Request', (object,), {'query_params': {}})
        response_without_filter = get_purchase_orders_list(request_without_filter)
        self.assertEqual(response_without_filter.status_code, 200)
        self.assertEqual(len(response_without_filter.data), 2)
        
        request_with_filter = type('Request', (object,), {'query_params': {'vendor_id': vendor1.id}})
        response_with_filter = get_purchase_orders_list(request_with_filter)
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertEqual(len(response_with_filter.data), 1)

    def test_get_purchase_order_detail(self):
            
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123', 
            vendor=vendor, 
            order_date=timezone.now(), 
            delivery_date=timezone.now(), 
            items={},
            quantity=1,
            status='completed',          
            quality_rating=4,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
            )

        request = type('Request', (object,), {})
        response = get_purchase_order_detail(request, purchase_order.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['po_number'], 'PO123')

    def test_update_purchase_order(self):
        vendor = Vendor.objects.create(
            name="Amitabh Bachchan",
            contact_details="0987654321",
            address="Baner, Pune",
            vendor_code="ABP",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfilment_rate=0.0
        )
        purchase_order = PurchaseOrder.objects.create(
            po_number="987",
            order_date="2023-11-29T21:39:04Z",
            delivery_date="2023-11-29T18:00:00Z",
            items={"Biscuits": "Parle-G", "Namkeen": "Aloo Bhujia"},
            quantity=10,
            status="pending",
            quality_rating=10.8,
            issue_date="2023-11-29T09:28:24.898025Z",
            acknowledgment_date="2023-11-29T09:28:24.898041Z",
            vendor=vendor
        )

        data = {
            "id": purchase_order.id,
            "po_number": "278",
            "order_date": "2023-11-29T21:39:04Z",
            "delivery_date": "2023-11-29T18:00:00Z",
            "items": {"Soap": "Liril", "Detergent": "Surf Excel", "Bathroom Cleaner": "Harpic"},
            "quantity": 5,
            "status": "pending",
            "quality_rating": 23.5,
            "issue_date": "2023-11-29T12:35:21.981503Z",
            "acknowledgment_date": "2023-11-29T12:35:21.981539Z",
            "vendor": vendor.id  # Update with vendor.id
        }

        request = type('Request', (object,), {'data': data})
        response = update_purchase_order(request, purchase_order.id)
        self.assertEqual(response.status_code, 200)

        purchase_order.refresh_from_db()
        self.assertEqual(purchase_order.po_number, '278')  # Update expected po_number
        self.assertEqual(purchase_order.status, 'pending')  # Update expected status

    def test_delete_purchase_order(self):
            
        vendor = Vendor.objects.create(
            name="Test Vendor", 
            contact_details="Contact",
            address="Address", 
            vendor_code="V1"
            )
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123', 
            vendor=vendor, 
            order_date=timezone.now(), 
            delivery_date=timezone.now(), 
            items={},
            quantity=1,
            status='completed',          
            quality_rating=4,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
            )

        request = type('Request', (object,), {})
        response = delete_purchase_order(request, purchase_order.id)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(PurchaseOrder.DoesNotExist):
            PurchaseOrder.objects.get(id=purchase_order.id)
            
    def test_get_historical_performance_detail(self):
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")
        
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.2,
            average_response_time=15.0,
            fulfilment_rate=0.95,
        )
        
        request = type('Request', (object,), {})  
        response = get_historical_performance_detail(request, vendor.id)        
        
        historical_performance_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(historical_performance_data), 1)  
        self.assertEqual(historical_performance_data[0]['on_time_delivery_rate'], 0.8)        
        self.assertEqual(historical_performance_data[0]['quality_rating_avg'], 4.2)
        self.assertEqual(historical_performance_data[0]['average_response_time'], 15.0)
        self.assertEqual(historical_performance_data[0]['fulfilment_rate'], 0.95)
        
        non_existing_vendor_id = 999  
        response_no_data = get_historical_performance_detail(request, non_existing_vendor_id)
        self.assertEqual(response_no_data.status_code, 200)
                
# class VendorTestCase(TestCase):
    def test_update_vendor_metrics(self):        
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address", vendor_code="V1")
                
        purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={},
            quantity=1,
            status='completed',
            quality_rating=4,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )
        
        update_vendor_metrics(vendor)
        
        vendor.refresh_from_db()
        
        self.assertEqual(vendor.on_time_delivery_rate, 1.0)
        self.assertEqual(vendor.quality_rating_avg, 4.0)
        self.assertEqual(round(vendor.average_response_time, 2), 0.0)  
        self.assertEqual(vendor.fulfilment_rate, 1.0)


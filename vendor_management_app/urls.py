from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/vendors/', views.get_vendors, name='vendors'),    
    path('api/vendors/<str:pk>/', views.get_vendor, name='vendor'),
    path('api/purchase_orders/', views.get_purchase_orders, name='purchase_orders'),
    path('api/purchase_orders/<str:pk>/', views.get_purchase_order, name='purchase_order'),
    path('api/vendors/<str:pk>/performance/', views.get_historical_performance, name='historical_performance'),
    path('api/purchase_orders/<str:pk>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
    path('logout/', views.admin_logout, name='logout'),
]
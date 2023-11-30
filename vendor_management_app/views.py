from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .services import (create_vendor, get_vendor_list, get_vendor_detail, update_vendor, delete_vendor,
create_purchase_order, get_purchase_orders_list, update_purchase_order, delete_purchase_order,
get_purchase_order_detail, get_historical_performance_detail, acknowledge_purchase_order_services)

# User authentication
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('login') 

#  Django REST Framework APIs

@login_required
@api_view(['GET', 'POST'])
def get_vendors(request):
    if request.method == 'GET':
        return get_vendor_list(request)
        
    if request.method == 'POST':
        return create_vendor(request)    

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def get_vendor(request, pk):
    if request.method == 'GET': 
        return get_vendor_detail(request, pk)
            
    if request.method == 'PUT':
        return update_vendor(request, pk)
            
    if request.method == 'DELETE':
        return delete_vendor(request, pk)     

@login_required    
@api_view(['GET', 'POST'])
def get_purchase_orders(request):
    if request.method == 'GET':
        return get_purchase_orders_list(request)
        
    if request.method == 'POST':
        return create_purchase_order(request)  

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def get_purchase_order(request, pk):
    if request.method == 'GET': 
        return get_purchase_order_detail(request, pk)
            
    if request.method == 'PUT':
        return update_purchase_order(request, pk)
            
    if request.method == 'DELETE':
        return delete_purchase_order(request, pk)    
    
@login_required
@api_view(['GET'])
def get_historical_performance(request, pk):
    if request.method == 'GET': 
        return get_historical_performance_detail(request, pk)
    
@login_required
@api_view(['POST'])
def acknowledge_purchase_order(request, pk):
    if request.method == 'POST': 
        return acknowledge_purchase_order_services(request, pk)
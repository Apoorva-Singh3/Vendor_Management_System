# Vendor_Management_System
A Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics

## Task
1. Vendor Profile Management:
  Create a model to store vendor info with CRUD API endpoints.
  Endpoints include creating, listing, retrieving, updating, and deleting vendors.

2.Purchase Order Tracking:
  Model for tracking purchase orders with relevant fields.
  API endpoints for creating, listing, retrieving, updating, and deleting purchase orders.
  
3.Vendor Performance Evaluation:
  Metrics include On-Time Delivery Rate, Quality Rating, Response Time, and Fulfilment Rate.
  Add fields to the vendor model to store performance metrics.
  Endpoint to retrieve a vendor's performance metrics.
  
4.Data Models:
  Vendor Model with essential fields.
  Purchase Order Model capturing order details.
  Historical Performance Model for trend analysis.
  
5.Backend Logic for Performance Metrics:
  On-Time Delivery Rate calculated on completed POs.
  Quality Rating Average updated on each PO completion with a rating.
  Average Response Time calculated on PO acknowledgment.
  Fulfilment Rate calculated on any change in PO status.
  
6.API Endpoint Implementation:
  Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance) retrieves calculated metrics.
  Consider an Update Acknowledgment Endpoint (POST /api/purchase_orders/{po_id}/acknowledge).

## Project Setup
1. Go to the GitHub repository
2. Copy the URL for the repository
3. Install Git in local machine
4. Open GitBash terminal
5. Change the current working directory to the location where you want the cloned directory
6. Type git clone, and then paste the URL you copied earlier
7. Press Enter to create your local clone
8. Open the project in VS Code IDE or any other of your preference
9. Open terminal in your IDE
10. Install 'pip install virtualenv'(assuming Python is installed in the system)
11. Create virtual environment for the project using 'virtualenv {virtual environment name}'
12. Activate virtual enviroment using:
    source {virtual environment name}/bin/activate	- Ubuntu
    {virtual environment name}\Scripts\activate	- Windows
13. Install dependencies using 'pip install -r requirements.txt'

## Instruction for Running Test Suite
1. Open the terminal in your IDE
2. Activate virtual environment using :
   source {virtual environment name}/bin/activate	- Ubuntu
    {virtual environment name}\Scripts\activate	- Windows
4. Change directory to the project root directory
5. Run test suite using "python manage.py test"

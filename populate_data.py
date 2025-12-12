import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i_m_s_project.settings')
django.setup()

from i_m_s_app.models import Category, Unit, Vendor, Product, Customer, Sale

def populate():
    print("Populating data...")

    # 1. Units
    units = ['kg', 'pc', 'box', 'liter', 'meter']
    unit_objs = []
    for u in units:
        obj, created = Unit.objects.get_or_create(name=u)
        unit_objs.append(obj)
    print(f"Created {len(unit_objs)} Units")

    # 2. Categories
    categories = ['Electronics', 'Groceries', 'Clothing', 'Furniture', 'Stationery']
    cat_objs = []
    for c in categories:
        obj, created = Category.objects.get_or_create(name=c, defaults={'description': f'All kinds of {c}'})
        cat_objs.append(obj)
    print(f"Created {len(cat_objs)} Categories")

    # 3. Vendors
    vendors_data = [
        {'name': 'TechSupplies Inc', 'email': 'contact@techsupplies.com', 'phone': '1234567890'},
        {'name': 'FreshFarms Ltd', 'email': 'sales@freshfarms.com', 'phone': '0987654321'},
        {'name': 'Global Traders', 'email': 'info@globaltraders.com', 'phone': '1122334455'},
    ]
    for v in vendors_data:
        Vendor.objects.get_or_create(
            name=v['name'],
            defaults={
                'vendor_id': f"V-{random.randint(1000, 9999)}",
                'email': v['email'],
                'phone': v['phone'],
                'address': '123 Sample St, City',
                'other_details': 'Preferred supplier'
            }
        )
    print(f"Created {len(vendors_data)} Vendors")

    # 4. Products
    products_data = [
        ('Laptop', 'Electronics', 'pc', 45000, 55000),
        ('Smartphone', 'Electronics', 'pc', 15000, 20000),
        ('Rice', 'Groceries', 'kg', 40, 60),
        ('Wheat', 'Groceries', 'kg', 30, 45),
        ('Notebook', 'Stationery', 'pc', 50, 80),
        ('Pen Box', 'Stationery', 'box', 100, 150),
        ('T-Shirt', 'Clothing', 'pc', 200, 400),
        ('Jeans', 'Clothing', 'pc', 600, 1200),
        ('Office Chair', 'Furniture', 'pc', 3000, 5000),
        ('Desk', 'Furniture', 'pc', 4000, 7000),
    ]

    prod_objs = []
    for name, cat_name, unit_name, p_price, s_price in products_data:
        cat = Category.objects.get(name=cat_name)
        unit = Unit.objects.get(name=unit_name)
        obj, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'sku': f"SKU-{random.randint(10000, 99999)}",
                'category': cat,
                'unit': unit,
                'stock': Decimal(random.randint(5, 50)),
                'purchase_price': Decimal(p_price),
                'selling_price': Decimal(s_price),
                'description': f"High quality {name}"
            }
        )
        prod_objs.append(obj)
    print(f"Created {len(prod_objs)} Products")

    # 5. Customers
    customers = ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'David Wilson']
    cust_objs = []
    for c in customers:
        obj, created = Customer.objects.get_or_create(
            name=c,
            defaults={'email': f"{c.replace(' ', '').lower()}@example.com", 'phone': '555-0100'}
        )
        cust_objs.append(obj)
    print(f"Created {len(cust_objs)} Customers")

    # 6. Sales (Recent Transactions)
    # Create some sales for today and past days
    for _ in range(10):
        prod = random.choice(prod_objs)
        qty = Decimal(random.randint(1, 5))
        
        # Ensure stock doesn't go negative for the sample
        if prod.stock >= qty:
            Sale.objects.create(
                product=prod,
                customer=random.choice(cust_objs),
                quantity=qty,
                sale_price=prod.selling_price,
                total_price=qty * prod.selling_price,
                remarks='Sample sale'
            )
            # Note: The model save() method automatically deducts stock, 
            # so we don't need to manually update it here if relying on save(),
            # but usually bulk creation skips save(). Here we use create() so save() is called.

    print("Created 10 Sample Sales")
    print("Data population complete!")

if __name__ == '__main__':
    populate()

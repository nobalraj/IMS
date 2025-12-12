from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from i_m_s_app.models import Product, Vendor, Sale

@login_required
def dashboard(request):
    # Total Products
    total_products = Product.objects.count()
    
    # Verified Vendors
    total_vendors = Vendor.objects.count()
    
    # Stock Alerts (e.g., products with stock < 10)
    stock_alerts = Product.objects.filter(stock__lt=10).count()
    
    # Today's Sales
    today = timezone.now().date()
    # Assuming 'total_price' is a field in Sale, or we sum 'quantity' * 'sale_price' if field doesn't exist
    # Based on models provided, Sale has total_price field.
    todays_sales_agg = Sale.objects.filter(sale_date=today).aggregate(
        total_sales=Sum('total_price')
    )
    todays_sales = todays_sales_agg['total_sales'] or 0
    
    # Recent Sales
    recent_sales = Sale.objects.select_related('product', 'customer').order_by('-sale_date', '-id')[:5]
    
    context = {
        'total_products': total_products,
        'total_vendors': total_vendors,
        'stock_alerts': stock_alerts,
        'todays_sales': todays_sales,
        'recent_sales': recent_sales,
    }
    
    return render(request, 'dashboard.html', context)
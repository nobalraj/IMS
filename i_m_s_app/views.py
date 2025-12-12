from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .models import *
from .forms import PurchaseForm
from . import views

def index(request):
    return render(request,'index.html')

class vendor_post_view(ListView):
    model=Vendor
    template_name='vendor.html'

    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Vendor.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(vendor_id__icontains=query)
            )
        return Vendor.objects.all()
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        # Handle Edit
        if action == 'edit':
            vendor_id = request.POST.get('vendor_id')
            try:    
                vendor = Vendor.objects.get(pk=vendor_id)
                vendor.name = request.POST.get('name')
                vendor.email = request.POST.get('email')
                vendor.phone = request.POST.get('phone')
                vendor.address = request.POST.get('address')
                vendor.other_details = request.POST.get('other_details')
                vendor.is_active = request.POST.get('is_active') == 'on'
                vendor.save()
                messages.success(request, "Vendor updated successfully!")
            except Vendor.DoesNotExist:
                messages.error(request, "Vendor not found!")
            except Exception as e:
                messages.error(request, f"Error updating vendor: {e}")
        
        # Handle Delete
        elif action == 'delete':
            vendor_id = request.POST.get('vendor_id')
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                vendor_name = vendor.name
                vendor.delete()
                messages.success(request, f"Vendor '{vendor_name}' deleted successfully!")
            except Vendor.DoesNotExist:
                messages.error(request, "Vendor not found!")
            except Exception as e:
                messages.error(request, f"Error deleting vendor: {e}")
        
        # Handle Add (default)
        else:
            try:
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                other_details = request.POST.get('other_details')
                vendor_id = request.POST.get('vendor_id')
                is_active = request.POST.get('is_active') == 'on'
                
                vendor = Vendor(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    other_details=other_details,
                    vendor_id=vendor_id,
                    is_active=is_active
                )
                vendor.save()
                messages.success(request, "Vendor added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding vendor: {e}")
        
        return redirect('vendor')

class product_post_view(ListView):
    model = Product
    template_name = 'product.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        queryset = Product.objects.all()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query) |
                Q(category__name__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['units'] = Unit.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        action=request.POST.get('action')
        if action == 'edit':
            product_id=request.POST.get('product_id')
            try:
                product=Product.objects.get(pk=product_id)
                product.name=request.POST.get('name')
                product.sku=request.POST.get('sku')
                product.category_id=request.POST.get('category')
                product.unit_id=request.POST.get('unit')
                product.purchase_price=request.POST.get('purchase_price')
                product.selling_price=request.POST.get('selling_price')
                product.stock=request.POST.get('stock')
                product.is_active=request.POST.get('is_active')=='on'
                product.description=request.POST.get('description')
                product.save()
                messages.success(request,"Product updated successfully!")
            except Product.DoesNotExist:
                messages.error(request,"Product not found!")
            except Exception as e:
                messages.error(request,f"Error updating product: {e}")
        elif action == 'delete':
            product_id=request.POST.get('product_id')
            try:
                product=Product.objects.get(pk=product_id)
                product_name=product.name
                product.delete()
                messages.success(request,f"Product '{product_name}' deleted successfully!")
            except Product.DoesNotExist:
                messages.error(request,"Product not found!")
            except Exception as e:
                messages.error(request,f"Error deleting product: {e}")
        else:
            try:
                name = request.POST.get('name')
                sku = request.POST.get('sku')
                category_id = request.POST.get('category')
                unit_id = request.POST.get('unit')
                purchase_price = request.POST.get('purchase_price')
                selling_price = request.POST.get('selling_price')
                stock = request.POST.get('stock')
                is_active = request.POST.get('is_active') == 'on'
                description = request.POST.get('description')
            
                product = Product(
                name=name,
                sku=sku,
                category_id=category_id,
                unit_id=unit_id,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock=stock,
                is_active=is_active,
                description=description
                )
                product.save()
                messages.success(request, "Product added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding product: {e}")
             
        return redirect('product')

class unit_post_view(ListView):
    model=Unit
    template_name='unit.html'

    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Unit.objects.filter(
                Q(name__icontains=query) |
                Q(title__icontains=query)
            )
        return Unit.objects.all()
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        # Handle Edit
        if action == 'edit':
            unit_id = request.POST.get('unit_id')
            try:
                unit = Unit.objects.get(pk=unit_id)
                unit.name = request.POST.get('name')
                unit.title = request.POST.get('title')
                unit.save()
                messages.success(request, "Unit updated successfully!")
            except Unit.DoesNotExist:
                messages.error(request, "Unit not found!")
            except Exception as e:
                messages.error(request, f"Error updating unit: {e}")
        
        # Handle Delete
        elif action == 'delete':
            unit_id = request.POST.get('unit_id')
            try:
                unit = Unit.objects.get(pk=unit_id)
                unit_name = unit.name
                unit.delete()
                messages.success(request, f"Unit '{unit_name}' deleted successfully!")
            except Unit.DoesNotExist:
                messages.error(request, "Unit not found!")
            except Exception as e:
                messages.error(request, f"Error deleting unit: {e}")
        
        # Handle Add (default)
        else:
            try:
                name = request.POST.get('name')
                title = request.POST.get('title')
                unit = Unit(name=name, title=title)
                unit.save()
                messages.success(request, "Unit added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding unit: {e}")
        
        return redirect('unit')


class purchase_post_view(ListView):
    model = Purchase
    template_name = 'purchase.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Purchase.objects.filter(
                Q(product__name__icontains=query) |
                Q(vendor__name__icontains=query) |
                Q(remarks__icontains=query)
            )
        return Purchase.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PurchaseForm()
        return context
        
    def post(self, request, *args, **kwargs):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Purchase added successfully!")
                return redirect('purchase')
            except Exception as e:
                messages.error(request, f"Error adding purchase: {e}")
        else:
             messages.error(request, "Error adding purchase. Please check the form.")
             
        return redirect('purchase')


class customer_post_view(ListView):
    model = Customer
    template_name = 'customer.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Customer.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )
        return Customer.objects.all().order_by('-created_at')
    
    def post(self, request, *args, **kwargs):
        from .forms import CustomerForm
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Customer added successfully!")
                return redirect('customer')
            except Exception as e:
                messages.error(request, f"Error adding customer: {e}")
        else:
            messages.error(request, "Error adding customer. Please check the form.")
        
        return redirect('customer')



class category_post_view(ListView):
    model = Category
    template_name = 'category.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Category.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return Category.objects.all().order_by('name')
    
    def post(self, request, *args, **kwargs):
        from .forms import CategoryForm
        action = request.POST.get('action')
        
        # Handle Edit
        if action == 'edit':
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(pk=category_id)
                form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Category updated successfully!")
                else:
                    messages.error(request, "Error updating category. Please check the form.")
            except Category.DoesNotExist:
                messages.error(request, "Category not found!")
            except Exception as e:
                messages.error(request, f"Error updating category: {e}")
        
        # Handle Delete
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(pk=category_id)
                category_name = category.name
                category.delete()
                messages.success(request, f"Category '{category_name}' deleted successfully!")
            except Category.DoesNotExist:
                messages.error(request, "Category not found!")
            except Exception as e:
                messages.error(request, f"Error deleting category: {e}")
        
        # Handle Add (default)
        else:
            form = CategoryForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Category added successfully!")
                except Exception as e:
                    messages.error(request, f"Error adding category: {e}")
            else:
                messages.error(request, "Error adding category. Please check the form.")
        
        return redirect('category')



class sale_post_view(ListView):
    model = Sale
    template_name = 'sale.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        if query:
            return Sale.objects.filter(
                Q(product__name__icontains=query) |
                Q(customer__name__icontains=query) |
                Q(remarks__icontains=query)
            )
        return Sale.objects.all().order_by('-sale_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import SaleForm
        context['form'] = SaleForm()
        return context
        
    def post(self, request, *args, **kwargs):
        from .forms import SaleForm
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Sale recorded successfully!")
                return redirect('sale')
            except Exception as e:
                messages.error(request, f"Error recording sale: {e}")
        else:
             messages.error(request, "Error recording sale. Please check the form.")
             
        return redirect('sale')





def order_get(request):
    return render(request,'order.html')

def order_post(request):
    if request.method=="POST":
        product_name=request.POST['product_name']
        messages.info(request,"product_name :" + product_name)
        request.session['product_name']=product_name
        
        amount=request.POST['amount']
        messages.info(request,"Amount :" + amount)
        request.session['amount']=amount
        
        
    return  views.index(request)


def invoice(request):
    product_name=request.session['product_name']
    amount=request.session['amount']
    
    return render(request,"invoice.html",\
        {'product_name':product_name,'amount':amount},)
    
    
# def vendor_view_get(request):
#     return render(request,'vendor.html')
    
'''Inventory Management System '''
def base_view(request):
    return render(request,'base/base.html')

def sidebar(request):
    return render(request,'base/aidebar.html')


def dashboard(request):
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Get current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    # Total counts
    total_products = Product.objects.count()
    total_vendors = Vendor.objects.count()
    total_customers = Customer.objects.count()
    total_categories = Category.objects.count()
    
    # Active vendors
    active_vendors = Vendor.objects.filter(is_active=True).count()
    
    # Purchases stats
    total_purchases = Purchase.objects.count()
    this_month_purchases = Purchase.objects.filter(
        purchase_date__month=current_month,
        purchase_date__year=current_year
    ).count()
    total_purchase_value = Purchase.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Sales stats
    total_sales = Sale.objects.count()
    this_month_sales = Sale.objects.filter(
        sale_date__month=current_month,
        sale_date__year=current_year
    ).count()
    total_sales_revenue = Sale.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Low stock products (stock less than 10)
    low_stock_products = Product.objects.filter(stock__lt=10).count()
    
    # Recent activities
    recent_purchases = Purchase.objects.all().order_by('-purchase_date')[:5]
    recent_sales = Sale.objects.all().order_by('-sale_date')[:5]
    
    # Product stock value
    products = Product.objects.all()
    total_stock_value = sum([(p.stock * p.selling_price) for p in products])
    
    context = {
        'total_products': total_products,
        'total_vendors': total_vendors,
        'total_customers': total_customers,
        'total_categories': total_categories,
        'active_vendors': active_vendors,
        'total_purchases': total_purchases,
        'this_month_purchases': this_month_purchases,
        'total_purchase_value': total_purchase_value,
        'total_sales': total_sales,
        'this_month_sales': this_month_sales,
        'total_sales_revenue': total_sales_revenue,
        'low_stock_products': low_stock_products,
        'recent_purchases': recent_purchases,
        'recent_sales': recent_sales,
        'total_stock_value': total_stock_value,
        'current_month_name': now.strftime('%B'),
    }
    
    return render(request, 'dashboard.html', context)
    
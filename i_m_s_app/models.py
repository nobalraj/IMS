from django.db import models
# Import Decimal for accurate monetary/quantity calculations
from decimal import Decimal 
from django.core.exceptions import ValidationError

# Create your models here.

class Vendor(models.Model):
    # Added max_length to CharField fields
    vendor_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    # Changed phone to CharField for better handling of formats (+, -, spaces) and added max_length
    phone = models.CharField(max_length=15, blank=True, null=True)
    # Added max_length to these CharFields (or consider using TextField as previously suggested)
    address = models.CharField(max_length=255, blank=True)
    other_details = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural='1.Vendor'   
    
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    # 'title' field seems redundant if 'name' is the main descriptor.
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural='2.Unit'
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Description field is correctly TextField now
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural='3.Category'
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Use Decimal('0.00') for robust default values
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    stock = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal('0.000'))
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    class Meta:
        # Typo fixed
        verbose_name_plural = '4.Product'
    
    def __str__(self):
        return f"{self.name}({self.sku})" 
        
    @property
    def profit_margin(self):
        # Calculation is fine
        if self.purchase_price > 0:
            return (self.selling_price - self.purchase_price) / self.purchase_price * 100
        return 0.0  
    
    
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True) 
    
    class Meta:
        verbose_name_plural = "5. Purchase"
        
    def save(self, *args, **kwargs):
        if not self.total_price:
           self.total_price = self.quantity * self.purchase_price
        
        super().save(*args, **kwargs)
        
        # Use Decimal() wrapper when converting to ensure precision in stock update
        product_instance = self.product
        product_instance.stock += Decimal(str(self.quantity))
        product_instance.save()

    def __str__(self):
        return f"{self.product.name} - {self.vendor.name} ({self.quantity})"
    
class Customer(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    # Added max_length for phone CharField
    phone = models.CharField(max_length=15, blank=True, null=True) 
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "6. Customer"
        # Removed managed=False so Django creates/manages this table
        
    def __str__(self):
        return self.name
    
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    sale_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "7. Sales"

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValidationError(f"Insufficient stock for {self.product.name}. Current stock: {self.product.stock}")
            
        if not self.total_price:
            self.total_price = self.quantity * self.sale_price
            
        super().save(*args, **kwargs)
        
        # Use Decimal() wrapper when converting to ensure precision in stock update
        product_instance = self.product
        product_instance.stock -= Decimal(str(self.quantity))
        product_instance.save()

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Walk-in Customer"
        return f"{self.product.name} sold to {customer_name} ({self.quantity})"

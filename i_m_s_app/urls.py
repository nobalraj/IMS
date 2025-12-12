
from django.urls import path ,re_path

from.views import vendor_post_view




from . import views
# from views import *
urlpatterns=[
    # path('',views.index,name="index"),
    # path('index',views.index,name='index'),
    # path('hello',views.hello,name='hello')
    # re_path(r'(?i)order/',views.order_get,name='order'),
    # re_path(r'(?i)order_post/',views.order_post),
    # re_path(r'(?i)invoice/',views.invoice)
    
    # inventory management system
    
    # re_path(r'vendor/',views.vendor_view_get,name='vendor')
    # path('base/',views.base_view,name='base'),
    # path('sidebar/',views.sidebar,name='sidebar'),
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alt'),
    
    path('vendor/',vendor_post_view.as_view(),name='vendor'),
    path('product/',views.product_post_view.as_view(),name='product'),
    path('unit/',views.unit_post_view.as_view(),name='unit'),
    path('purchase/',views.purchase_post_view.as_view(),name='purchase'),
    path('customer/',views.customer_post_view.as_view(),name='customer'),
    path('category/',views.category_post_view.as_view(),name='category'),
    path('sale/',views.sale_post_view.as_view(),name='sale'),
]
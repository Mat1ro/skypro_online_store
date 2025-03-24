from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductListView, ProductDetailView, ContactUsView, ProductCreateView, ProductUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('contact_us', ContactUsView.as_view(), name='contact_us'),
    path('create_product', ProductCreateView.as_view(), name='product_create'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
]

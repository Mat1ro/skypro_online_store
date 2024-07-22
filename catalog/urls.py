from django.conf.urls.static import static
from django.urls import path

from catalog.views import main, product_detail
from skypro_online_store import settings

urlpatterns = [
    path('', main, name='product_list'),
    path('product/<int:product_id>', product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path

from catalog.views import main, contact

urlpatterns = [
    path('', main),
    path('contact/', contact)
]

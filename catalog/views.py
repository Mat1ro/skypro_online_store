from pprint import pprint

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем данные об активных версиях продуктов
        products_with_versions = []
        for product in context['products']:
            active_version = Version.objects.filter(product=product, current_version=True).first()

            # Добавляем продукт с активной версией в новый список
            products_with_versions.append({
                'product': product,
                'active_version': active_version,
            })

        # Обновляем контекст для шаблона
        context['products_with_versions'] = products_with_versions
        pprint(context)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'product_create.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.id])


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

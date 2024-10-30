from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
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
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'product_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user:
            return HttpResponseForbidden(
                "Вы не можете редактировать этот продукт, так как вы не являетесь его владельцем.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.id])


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

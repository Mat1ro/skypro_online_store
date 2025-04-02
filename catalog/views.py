from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Product, Version
from catalog.services import get_categories


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
        context['categories'] = get_categories()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        product = self.get_object()

        context['is_owner'] = product.owner == user
        context['is_manager'] = user.groups.filter(name='manager').exists()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'product_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    permission_required = [
        'catalog.can_change_description',
        'catalog.can_change_category',
        'catalog.can_change_is_published'
    ]

    def has_permission(self):
        product = self.get_object()
        if product.owner == self.request.user:
            return True
        return super().has_permission()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        user = self.request.user

        if self.object.owner == user:
            return form

        if user.groups.filter(name='manager').exists():
            allowed_fields = ['description', 'category', 'is_published']
            form.fields = {key: form.fields[key] for key in allowed_fields if key in form.fields}

        return form

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.id])


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

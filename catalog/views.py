from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def main(request):
    context = {
        'object_list': Product.objects.all()
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
    context = {
        'product': get_object_or_404(Product, id=product_id)
    }
    return render(request, 'product_detail.html', context)

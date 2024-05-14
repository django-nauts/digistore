from django.shortcuts import render, get_object_or_404

from app_product.models import Product


# Create your views here.

def product_list(request):
    return render(request, 'app_product/product_list.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True, in_stock=True)
    context = {
        'product': product
    }
    return render(request, 'app_product/product_detail.html', context)

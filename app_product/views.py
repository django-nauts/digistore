from django.shortcuts import render

# Create your views here.

def product_list(request):
    return render(request, 'app_product/product_list.html')

def product_detail(request):
    return render(request, 'app_product/product_detail.html')
from django.shortcuts import render

# Create your views here.


def about_us(request):
    return render(request, 'app_site_setting/about_us.html')

def contact_us(request):
    return render(request, 'app_site_setting/contact_us.html')

def faq(request):
    return render(request, 'app_site_setting/faq.html')
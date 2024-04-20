from django.urls import path
from . import views

app_name = 'app_site_setting'

urlpatterns = [
    path('about-us/', views.about_us, name='about_us_page'),
    path('contact-us/', views.contact_us, name='contact_us_page'),
    path('faq/', views.faq, name='faq_page'),

]
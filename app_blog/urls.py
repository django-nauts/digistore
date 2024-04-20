from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list_page'),
    path('detail/', views.blog_detail, name='blog_detail_page'),
]
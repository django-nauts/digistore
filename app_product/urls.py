from django.urls import path
from .views import (
	ProductListView,
	ProductDetailView,
	ProductCreateView,
	ProductUpdateView,
	ProductDeleteView,
	ProductCategoryView,
)

app_name = 'app_product'

urlpatterns = [
	path('create/', ProductCreateView.as_view(), name='product_create'),
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/edit', ProductUpdateView.as_view(), name='product_edit'),
    path('<slug:slug>/delete', ProductDeleteView.as_view(), name='product_delete'),
	path('category/<slug:tag_slug>/', ProductCategoryView.as_view(), name='product_category'),
]

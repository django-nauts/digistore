from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
	ProductAPIListView,
	ProductAPIDetailView,
	UserAPIListView,
	UserAPIDetailView,
	UserViewSet,
	ProductViewSet,
)


urlpatterns = [
	path('product/', ProductAPIListView().as_view(), name='product_list'),
	path('product/<int:pk>/', ProductAPIDetailView.as_view(), name='product_detail'),
	path('users/', UserAPIListView.as_view()),
	path('users/<int:pk>/', UserAPIDetailView.as_view()),
]

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('product', ProductViewSet, basename='products')


urlpatterns = router.urls

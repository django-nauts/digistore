from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from app_blog.models import Post
from app_payment.models import Order, ShippingAddress
from app_product.models import Product, Category
# Create your views here.
from .serializers import ProductSerializer, CategorySerializer, PostSerializer, OrderSerializer, \
    ShippingAddressSerializer


# region app_payment

class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()

    def list(self, request):
        serializer = OrderSerializer(self.queryset.filter(user_id=request.user.id, is_paid=True), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = OrderSerializer(self.queryset.filter(user_id=request.user.id, pk=pk, is_paid=True), many=True)
        return Response(serializer.data)


class ShippingAddressViewSet(viewsets.ViewSet):
    queryset = ShippingAddress.objects.all()

    def list(self, request):
        serializer = ShippingAddressSerializer(self.queryset.filter(user_id=request.user.id), many=True)
        return Response(serializer.data)


# endregion

# region app_blog

class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()

    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = PostSerializer(self.queryset.filter(pk=pk), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# endregion

# region app_product
class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = ProductSerializer(self.queryset.filter(pk=pk), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'category/(?P<category>\w+)/all')
    def list_product_by_category(self, request, category=None):
        """
        To list products by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__name=category), many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

# endregion

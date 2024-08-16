from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from app_account.models import User
from app_blog.models import Post
from app_payment.models import Order, ShippingAddress
from .permissions import IsAuthor, IsSuperUserOrStaffReadOnly, IsUserOrSuperUser
from .serializers import PostSerializer, OrderSerializer, \
    ShippingAddressSerializer, UserSerializer


# Create your views here.


# region app_account

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrStaffReadOnly]


# endregion

# region app_payment

class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()

    @extend_schema(request=OrderSerializer, responses={201: OrderSerializer}, description='Display your order/s')
    @permission_classes([IsUserOrSuperUser])
    def list(self, request):
        if request.user.is_superuser:
            serializer = OrderSerializer(self.queryset.filter(is_paid=True), many=True)
        else:
            serializer = OrderSerializer(self.queryset.filter(user_id=request.user.id, is_paid=True), many=True)
        return Response(serializer.data)

    @permission_classes([IsUserOrSuperUser])
    @extend_schema(request=OrderSerializer, responses={201: OrderSerializer}, description='Display order by ID no.')
    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            serializer = OrderSerializer(self.queryset.filter(pk=pk, is_paid=True), many=True)
        else:
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

    @extend_schema(request=PostSerializer, responses={201: PostSerializer}, description='Add a new post')
    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=PostSerializer, responses={201: PostSerializer}, description='Add a new post')
    def retrieve(self, request, pk=None):
        serializer = PostSerializer(self.queryset.filter(pk=pk), many=True)
        return Response(serializer.data)

    # @action(detail=True, permission_classes=[IsAuthor])
    @extend_schema(request=PostSerializer, responses={201: PostSerializer}, description='Add a new post')
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=PostSerializer, responses={201: PostSerializer}, description='Add a new post')
    @permission_classes([IsAuthor])
    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthor])
    def destroy(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

# endregion

# region app_product
# endregion

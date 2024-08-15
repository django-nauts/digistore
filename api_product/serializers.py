from django.contrib.auth import get_user_model
from rest_framework import serializers

from app_product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('created_by', 'title', 'description', 'price')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_created_by(self, value):
        if not get_user_model().objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "username",)

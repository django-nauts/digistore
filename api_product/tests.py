# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from app_product.models import Product
from .serializers import ProductSerializer, UserSerializer

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.url = reverse('users-list')

    def test_create_user(self):
        data = {'username': 'newuser'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_list_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user(self):
        response = self.client.get(reverse('users-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        response = self.client.patch(reverse('users-detail', args=[self.user.id]), {'username': 'updateduser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_delete_user(self):
        response = self.client.delete(reverse('users-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(created_by=self.user, title='Test Product', description='Test Description', price=10.0)
        self.url = reverse('product_list')

    def test_create_product(self):
        data = {
            'created_by': self.user.id,
            'title': 'New Product',
            'description': 'New Description',
            'price': 20.0
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.product.title)

    def test_update_product(self):
        response = self.client.patch(reverse('product_detail', args=[self.product.id]), {'title': 'Updated Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product')

    def test_delete_product(self):
        response = self.client.delete(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_invalid_price(self):
        data = {
            'created_by': self.user.id,
            'title': 'Invalid Product',
            'description': 'Invalid Description',
            'price': -10.0
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Price must be a positive number.', response.data['price'])


class ProductSerializerTests(APITestCase):
    def test_valid_serializer(self):
        data = {
            'created_by': 1,
            'title': 'Valid Product',
            'description': 'Valid Description',
            'price': 10.0
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_price_serializer(self):
        data = {
            'created_by': 1,
            'title': 'Invalid Product',
            'description': 'Invalid Description',
            'price': -10.0
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Price must be a positive number.', serializer.errors['price'])

    def test_invalid_created_by_serializer(self):
        data = {
            'created_by': 999,
            'title': 'Invalid Product',
            'description': 'Invalid Description',
            'price': 10.0
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('User does not exist.', serializer.errors['created_by'])

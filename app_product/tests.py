from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from app_product.models import Product, Category
from app_product.views import ProductListView, ProductDetailView


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Test Category')
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.product = Product.objects.create(
            category=cls.category,
            created_by=cls.user,
            title='Test Product',
            description='Test Description',
            image='products/test_image.jpg',
            slug='test-product',
            price=10.00,
            is_sale=True,
            sale_price=8.00,
            in_stock=True,
            is_active=True
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertEqual(url, reverse('app_product:product_detail', kwargs={'slug': self.product.slug}))

    def test_product_fields(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.created_by, self.user)
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.image, 'products/test_image.jpg')
        self.assertEqual(self.product.slug, 'test-product')
        self.assertEqual(self.product.price, 10.00)
        self.assertTrue(self.product.is_sale)
        self.assertEqual(self.product.sale_price, 8.00)
        self.assertTrue(self.product.in_stock)
        self.assertTrue(self.product.is_active)

        
class ProductListViewTest(TestCase):
    def test_product_list_view(self):
        response = self.client.get(reverse('app_product:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_product/product_list.html')

        
class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Test Category')
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.product = Product.objects.create(
            category=cls.category,
            created_by=cls.user,
            title='Test Product',
            description='Test Description',
            image='products/test_image.jpg',
            slug='test-product',
            price=10.00,
            is_sale=True,
            sale_price=8.00,
            in_stock=True,
            is_active=True
        )

    def test_product_detail(self):
        response = self.client.get(reverse('app_product:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_product/product_detail.html')
        
    def test_post_createview(self):
        response = self.client.post(
            reverse("post_create"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New text")
        
    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "Updated title",
                "body": "Updated text",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated title")
        self.assertEqual(Post.objects.last().body, "Updated text")

    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)
    
        
class TestUrls(SimpleTestCase):
    def test_product_list_url_resolves(self):
        url = reverse('app_product:product_list')
        self.assertEqual(resolve(url).func.view_class, ProductList)

    def test_product_detail_url_resolves(self):
        url = reverse('app_product:product_detail', kwargs={'slug': 'test-product'})
        self.assertEqual(resolve(url).func.view_class, ProductDetail)


class PaginationTests(TestCase):
    def setUp(self):
        for i in range(15):
            Product.objects.create(full_name=f'Product {i+1}')

    def test_pagination_with_multiple_pages(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Page 1 of 2')
        self.assertQuerysetEqual(response.context['page_obj'].object_list, 
                                 Product.objects.all()[:10])

    def test_pagination_on_first_page(self):
        response = self.client.get(reverse('product_list') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')
        self.assertQuerysetEqual(response.context['page_obj'].object_list, 
                                 Product.objects.all()[:10])

    def test_pagination_on_last_page(self):
        response = self.client.get(reverse('product_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prev')
        self.assertNotContains(response, 'Next')
        self.assertQuerysetEqual(response.context['page_obj'].object_list, 
                                 Product.objects.all()[10:])

    def test_pagination_with_no_items(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No products available.')

    def test_pagination_links(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="?page=1"')
        self.assertContains(response, 'href="?page=2"')
        self.assertNotContains(response, 'href="?page=3"')

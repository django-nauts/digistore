from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_blog.models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.post = Post.objects.create(
            title="This is a title",
            body="This is main text",
            author=cls.user,
        )
        
    def test_post_model(self):
        self.assertEqual(self.post.title, "This is a title")
        self.assertEqual(self.post.slug, "this-is-a-title")
        self.assertEqual(self.post.body, "This is main text")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "This is a title")
        self.assertEqual(self.post.get_absolute_url(), "/blog/this-is-a-title")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/blog/this-is-a-title")
        self.assertEqual(response.status_code, 200)

    def test_blog_list_view(self):
        response = self.client.get(reverse('app_blog:blog_list'))
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view(self):
        post = Post.objects.create(title='Test Post', body='This is a test post')
        response = self.client.get(reverse('app_blog:blog_detail', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_template(self):
        response = self.client.get(reverse('app_blog:blog_list'))
        self.assertTemplateUsed(response, 'app_blog/blog_list.html')

    def test_blog_detail_template(self):
        post = Post.objects.create(title='Test Post', body='This is a test post')
        response = self.client.get(reverse('app_blog:blog_detail', kwargs={'slug': post.slug}))
        self.assertTemplateUsed(response, 'app_blog/blog_detail.html')

    def test_post_absolute_url(self):
        post = Post.objects.create(title='Test Post', body='This is a test post')
        self.assertEqual(post.get_absolute_url(), f'/blog/{post.slug}')

    def test_post_slug_generation(self):
        post = Post.objects.create(title='Test Post', body='This is a test post')
        self.assertIsNotNone(post.slug)

    def test_post_ordering(self):
        self.assertEqual(Post._meta.ordering, ['-publish'])

    def test_taggable_manager(self):
        post = Post.objects.create(title='Test Post', body='This is a test post')
        post.tags.add('tag1', 'tag2')
        self.assertEqual(post.tags.count(), 2)

    def test_post_createview(self):
        response = self.client.post(
            reverse("app_blog:post_new"),
            {
                "author": self.user.id,
                "title": "This is a title",
                "body": "This is main text",                
                "cover": "cover.jpg",
            },
        )
        self.assertEqual(Post.objects.last().title, "This is a title")
        self.assertEqual(Post.objects.last().body, "This is main text")

    def test_post_updateview(self):
        response = self.client.post(
            reverse("app_blog:post_edit", kwargs={'slug': self.post.slug}),
            {
            'title': 'This is a title',
            'body': 'This is main text',
            },
        )
        self.assertEqual(Post.objects.last().title, "This is a title")
        self.assertEqual(Post.objects.last().body, "This is main text")


    def test_blog_delete_view(self):
        response = self.client.post(reverse('app_blog:post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 302)  # Redirects to success_url


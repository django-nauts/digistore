from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Avg
from django.views import View
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from app_account.models import User 
from app_product.models import Product

from .forms import CommentForm


class ProductListView(ListView):
    model = Product
    template_name = 'app_product/product_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_products = Product.objects.count()
        current_page_products = len(context['object_list'])
        
        # Calculate average ratings for each product
        for product in context['object_list']:
            product.average_rating_value = product.average_rating()  # Get average rating
            product.total_comments = product.comment_set.count()  # Get total comments
        
        context['total_products'] = total_products
        context['current_page_products'] = current_page_products
        
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        product = self.object
        
        # Calculate average rating and total comments
        comments = product.comment_set.all()
        average_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0  # Default to 0 if no comments
        total_comments = comments.count()
        
        context['average_rating'] = average_rating * 20  # Convert to percentage for display (1-5 scale to 0-100)
        context['total_comments'] = total_comments
        
        # List of similar products based on tags
        product_tags_ids = product.tags.values_list('id', flat=True)
        similar_products = Product.objects.filter(
            tags__in=product_tags_ids
        ).exclude(id=product.id).annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-created')[:4]
        
        context['similar_products'] = similar_products
        
        # Get the previous and next products based on the created date
        previous_product = Product.objects.filter(created__lt=product.created).order_by('-created').first()
        next_product = Product.objects.filter(created__gt=product.created).order_by('created').first()
        
        context['previous_product'] = previous_product
        context['next_product'] = next_product
        
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'app_product/product_create.html'
    fields = ['title', 'description', 'image', 'price', 'tags']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'app_product/product_edit.html'
    fields = ['title', 'slug', 'description',
              'image','price', 'tags']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'app_product/product_delete.html'
    success_url = reverse_lazy('app_product:product_list')

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


# Show products with a specific category/tag
class ProductCategoryView(ListView):
    model = Product
    template_name = 'app_product/product_category.html'
    paginate_by = 6

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Product.objects.filter(tags__slug=tag_slug)

    # Show number of current and total products
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_products = Product.objects.count()
        current_page_products = len(context['object_list'])
        
        context['total_products'] = total_products
        context['current_page_products'] = current_page_products
        
        return context



class CommentGet(DetailView):
    model = Product
    template_name = "app_product/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Product
    form_class = CommentForm
    template_name = "app_product/product_detail.html"

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.author = request.user
            comment.save()
            comments_html = render_to_string('app_product/comments_list.html', {'comments': self.object.comment_set.all()})
            return JsonResponse({'success': True, 'comments_html': comments_html})
        return JsonResponse({'success': False, 'errors': form.errors})

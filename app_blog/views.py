from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, Page
from django.db.models import Count

from taggit.models import Tag

from .models import Post
from .forms import CommentForm


class BlogList(ListView):
    model = Post
    template_name = "app_blog/blog_list.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_tags'] = Tag.objects.all().order_by('-id')[:4]
        context['popular_posts'] = Post.objects.order_by('-views')[:4]

        return context


class CommentGet(DetailView):
    model = Post
    template_name = "app_blog/blog_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(FormView):
    model = Post
    form_class = CommentForm
    template_name = "app_blog/blog_detail.html"
    
    def form_valid(self, form):
        post = Post.objects.get(slug=self.kwargs['slug'])  # Retrieve the Post object using the slug from URL
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(slug=self.kwargs['slug'])  # Retrieve the Post object using the slug from URL
        return reverse("app_blog:blog_detail", kwargs={"slug": post.slug})




class BlogDetail(DetailView):
    model = Post
    template_name = "app_blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        post = self.get_object()
        
        # Get the current post's tags
        post_tags = post.tags.all()

        # Find posts with at least one tag in common with the current post
        similar_posts = Post.objects.filter(tags__in=post_tags).exclude(id=post.id).distinct()[:3]  # Adjust the number of similar posts as needed
        
        # Get comments related to the current post
        comments = post.comment_set.all()

        context['similar_posts'] = similar_posts
        context['comments'] = comments

        return context

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class BlogCreate(CreateView):
    model = Post
    template_name = "app_blog/post_new.html"
    fields = ["author", "title", "body", "cover", "tags"]


class BlogUpdate(UpdateView):
    model = Post
    template_name = "app_blog/post_edit.html"
    fields = fields = ["author", "title", "slug", "body", "cover", "tags"]


class BlogDelete(DeleteView):
    model = Post
    template_name = "app_blog/post_delete.html"
    success_url = reverse_lazy("app_blog:blog_list")

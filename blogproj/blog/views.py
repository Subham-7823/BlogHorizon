from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse



# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

def BlogUserProfileView(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'blog/blog_profile.html', {'user': user})

def about(request):
    return render(request, 'blog/about.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike
        liked = False
    else:
        post.likes.add(request.user)  # Like
        liked = True

    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})
    
    return redirect('blog-home')  # Redirect back to home

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# api request
import requests
from django.shortcuts import render

def latest_news(request):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",  # You can change to "us", "uk", etc.
        "apiKey": "b0ea3da1f00048f7a5824d60b86c6525",
        "pageSize": 5  # Number of news articles
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])

    return render(request, "blog/latest_news.html", {"articles": articles})

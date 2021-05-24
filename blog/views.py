from django.shortcuts import render
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Post, Category, Tag

#再利用可能なクラスベースのビューを、ジェネリックビューという。

class PostDetailView(DetailView):
    #queryset = Post.objects.all()と同義
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        #ユーザーがログインしていない且つ投稿が公開されていない場合にエラー
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"

class CategoryListView(ListView):
    #Tagオブジェクトと紐づくPostオブジェクトの個数を取得し、さらに公開されている投稿のみカウントする。
    #Qオブジェクトは複数のクエリをカプセル化するために使用される。１つのクエリのカプセル化にも使用可能。
    queryset = Tag.objects.annotate(num_posts=Count(
        "post", filter=Q(post__is_public=True)))

class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

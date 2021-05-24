from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #__str__:文字列を返すメソッド。adminでオブジェクトを分かりやすく表示する。
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    #ForeignKeyを使用して多対一の関係を作成
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    #ManyToManyFieldを使用して多対多の関係を作成
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    #下書きと公開済みの記事を区別する
    is_public = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    class Meta:
        #取得したオブジェクトを作成日時の降順で表示する
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            #初めて記事を公開する場合は現在の日時を保存する
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')

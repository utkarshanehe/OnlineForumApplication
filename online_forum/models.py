from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=512, unique=True, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to='authors', default=None, blank=False)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super(Author, self).save(self, *args, **kwargs)

    # Returns the number of posts posted by this author
    @property
    def number_of_posts(self):
        return Post.objects.filter(author=self).count()


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(default="Description")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts", kwargs={
            'slug': self.slug
        })

    # Returns the number of posts in this category
    @property
    def number_of_posts(self):
        return Post.objects.filter(categories=self).count()

    # Returns the last post in this category
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest('timestamp')


class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"


class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]


class Post(models.Model):
    title = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1500, unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    categories = models.ManyToManyField(Category)
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("post-detail", kwargs={
            'slug': self.slug
        })


from django.contrib import admin
from .models import Author, Category, Post, Reply, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Comment)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<slug>/', views.show_posts, name='posts'),
    path('post-detail/<slug>/', views.show_post_detail, name='post-detail'),
    path('create-post', views.create_post, name='create-post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('posts/', views.show_posts),
    path('post-detail/<slug>/', views.show_post_detail)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
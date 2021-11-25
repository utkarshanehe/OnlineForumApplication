from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_forum.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('account/', include('register_login.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
]

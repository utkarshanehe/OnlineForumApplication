from django.urls import path, include
from .views import signup, signin, update_profile, logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('update-profile/', update_profile, name='update-profile'),
    path('logout/', logout, name='logout'),
]

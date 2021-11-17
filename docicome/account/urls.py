from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
]
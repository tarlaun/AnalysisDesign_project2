from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('signin/', views.login, name='signin'),
]
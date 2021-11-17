from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('expertise_list/', views.ExpertiseView.as_view(), name='expertise_list')
]
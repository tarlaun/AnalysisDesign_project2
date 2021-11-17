from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('expertise_list/', views.ExpertiseView.as_view(), name='expertise_list'),
    path('expertise_list/<int:exp_id>/', views.request_for_chosen_expertise, name='req_for_exp')
]
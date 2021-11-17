from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    # پزشک :: نمایش درخواست‌های فعال موجود برای تخصص پزشک
    # پزشک :: قابلیت قبول درخواست
    path('expertise_orders_list/', views.expertise_orders_list, name='expertise_orders_list'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
]

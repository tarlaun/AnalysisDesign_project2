from django.urls import path
from . import views


urlpatterns = [
    # ورود و ثبت نام کاربر
    path('signup/', views.register, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    # پزشک :: نمایش درخواست‌های فعال موجود برای تخصص پزشک
    # پزشک :: قابلیت قبول درخواست
    path('expertise_orders_list/', views.expertise_orders_list, name='expertise_orders_list'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('expertise_list/', views.ExpertiseView.as_view(), name='expertise_list'),
    path('expertise_list/<int:exp_id>/', views.request_for_chosen_expertise, name='req_for_exp'),

    path('request_for_doc/<int:doc_id>/', views.request_for_chosen_doctor, name='req_for_doc'),
    path('add_order/<int:doc_id>/', views.add_order, name='add_order'),
    path('patient_orders_list/', views.patient_orders_list, name='patient_orders_list'),

    path('doctor_list/<int:exp_id>', views.doctor_list, name='doctor_list'),
    path('rate/', views.rate_order, name='rate-view'),
    path('comment/', views.comment_for_order, name='comment-view'),
    path('complaint/', views.complaint_for_order, name='complaint-view'),
    path('pre_orders/', views.previous_orders, name='pre_orders'),
    path('all_doctors/', views.all_doctors, name='all_doctors'),
    path('doctor_profile/<int:doc_id>/', views.doc_pro, name='doctor_profile'),
]

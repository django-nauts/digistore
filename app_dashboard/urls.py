from django.urls import path
from . import views

app_name = 'app_dashboard'

urlpatterns = [
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('change-info/', views.ChangeUserInfoView.as_view(), name='change_info_page'),
    path('<pk>/', views.Dashboard.as_view(), name='dashboard_page'),
]
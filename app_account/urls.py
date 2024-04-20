from django.urls import path
from . import views

app_name = 'app_account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forget-pass/', views.ForgetPasswordView.as_view(), name='forget_pass_page'),
    path('reset-pass/<email_active_code>/', views.ResetPasswordView.as_view(), name='reset_pass_page'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),

    # path('dashboard/', views.dashboard, name='dashboard_page'),
]
from django.urls import path
from . import views

app_name = 'userprofile' 
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Dashboard page
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path("register/", views.register, name="register"),  # Registration page
    path('logout/', views.logout, name='logout'),
    path('profile/update/', views.profile_update, name='profile-update'),  # Corrected name here
    path('update/success/', views.profile_update_success, name='profile_update_success'),
    path('update/error/', views.profile_update_error, name='profile_update_error'),
    path('transactions/', views.transaction_statement, name='transaction_statement'),
]

   



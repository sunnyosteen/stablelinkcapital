from django.urls import path
from . import views


app_name = 'investment'  # Define the app namespace here

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit_view'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal_view'),
    path('deposit/success/', views.deposit_success, name='deposit_success'),  # Correct this line
    path('withdrawal/success/', views.withdrawal_success, name='withdrawal_success'),
    path('error/', views.error_view, name='error_view'),  # Define the error_view here
    path('approve_transaction/<int:transaction_id>/', views.approve_transaction_view, name='approve_transaction_view'),
]

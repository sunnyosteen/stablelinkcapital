# connectwallet/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path('select-wallet/', views.select_wallet, name='select_wallet'),
     path('wallet-connection-success/', views.wallet_connection_success, name='wallet_connection_success'),
     path('error/', views.error_page, name='error_page'),  
]

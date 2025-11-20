
from django.contrib import admin
from .models import WalletAsset, ConnectWallet

class WalletAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'wallet_image', 'created_at', 'updated_at']  # Assuming these fields exist
    search_fields = ['name']
    list_filter = ['created_at', 'updated_at']  # Filter by creation and update date
    ordering = ['-created_at']  # Order by most recent entries first

class ConnectWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet', 'wallet_phrase', 'created_at', 'updated_at']  # Assuming these fields exist
    search_fields = ['user__username', 'wallet__name']
    list_filter = ['user', 'created_at', 'updated_at']  # Filter by user and dates
    ordering = ['-created_at']  # Order by most recent entries first

admin.site.register(WalletAsset, WalletAssetAdmin)
admin.site.register(ConnectWallet, ConnectWalletAdmin)

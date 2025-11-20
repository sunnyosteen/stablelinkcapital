

from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'phone_number', 'wallet_address', 'balance',
        'referral_code', 'used_referral_code', 'referral_reward',
        'date_of_birth', 'country', 'address', 'first_name', 'last_name'
    )
    search_fields = ['user__username', 'referral_code', 'used_referral_code', 'first_name', 'last_name']
    list_filter = ('country', 'date_of_birth')
    list_editable = ('phone_number', 'wallet_address', 'balance')

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'phone_number', 'wallet_address', 'date_of_birth', 'profile_image')
        }),
        ('Financial Information', {
            'fields': ('balance', 'referral_code', 'used_referral_code', 'referral_reward', 'return_of_investment', 'withdrawable_amount')
        }),
        ('Address Information', {
            'fields': ('country', 'address')
        }),
        ('Additional Information', {
            'fields': ('govt_issued_id', 'trading_certificates', 'selected_investment_plan', 'date')
        })
    )

    readonly_fields = ('date',)

admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin
from .models import InvestmentPlan, Transaction, Investment, WithdrawalRequest, Wallet

class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'duration_days', 'minimum_investment', 'maximum_investment')


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'deposit_amount', 'roi_accumulated', 'deposit_time', 'plan', 'is_active', 'end_date')

class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'amount', 'created_at', 'approved')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'wallet_address', 'icon')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'transaction_type', 'created_at')

    def approve_transaction(self, request, queryset):
        queryset.update(status='approved')
        for transaction in queryset:
            transaction.approve()

    approve_transaction.short_description = 'Approve selected transactions'

    actions = [approve_transaction]



# Register models with the admin site
admin.site.register(InvestmentPlan, InvestmentPlanAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(Wallet, WalletAdmin)

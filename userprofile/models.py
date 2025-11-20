


from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from decimal import Decimal
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = CountryField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Auto-generated unique referral code
    referral_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Code entered by user during registration (the one they used to get a reward)
    used_referral_code = models.CharField(max_length=100, blank=True, null=True)
    
    trading_certificates = models.ImageField(upload_to='trading_certificates/', blank=True, null=True)
    return_of_investment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now_add=True)
    withdrawable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    referral_reward = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    selected_investment_plan = models.ForeignKey(
        'investment.InvestmentPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    govt_issued_id = models.ImageField(upload_to='govt_issued_ids/', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def get_my_referrals(self):
        return UserProfile.objects.filter(
            used_referral_code=self.referral_code
        )


    

    def save(self, *args, **kwargs):
        # Auto-generate unique referral code
        if not self.referral_code or UserProfile.objects.filter(referral_code=self.referral_code).exclude(pk=self.pk).exists():
            self.referral_code = self.generate_unique_referral_code(self.user.username)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_referral_code(username):
        base = username[:6].upper()
        while True:
            suffix = uuid.uuid4().hex[:6].upper()
            code = f"{base}{suffix}"
            if not UserProfile.objects.filter(referral_code=code).exists():
                return code

    def calculate_withdrawable(self):
        self.withdrawable_amount = self.return_of_investment
        self.save()

    def calculate_return_of_investment(self, deposit_amount):
        if self.selected_investment_plan:
            self.return_of_investment = deposit_amount * (self.selected_investment_plan.interest_rate / Decimal('100'))
        else:
            self.return_of_investment = deposit_amount * Decimal('0.10')
        self.save()

    def update_balance(self, amount, transaction_type):
        if transaction_type == 'deposit':
            self.balance += amount
        elif transaction_type == 'withdrawal':
            self.balance -= amount
        self.save()

    def __str__(self):
        return f"{self.user.username} | Code: {self.referral_code} | Used: {self.used_referral_code}"

    

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

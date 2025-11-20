from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings




class InvestmentPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 for 10% ROI
    duration_days = models.IntegerField()  # Duration in days
    minimum_investment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    maximum_investment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Maximum investment allowed
    required_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.name} - {self.interest_rate}% ROI for {self.duration_days} days"

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investment Plans"





class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('roi', 'Return on Investment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of ${self.amount} by {self.user.username}"

    # -----------------------------------------------------
    #                USER EMAIL
    # -----------------------------------------------------
    def send_user_email(self, subject, template_name, extra_context=None):
        context = {
            "username": self.user.username,
            "amount": self.amount,
            "transaction_id": self.id,
            "approval_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "dashboard_url": "https://www.eversteadinvest.com/userprofile/dashboard/",
        }

        if extra_context:
            context.update(extra_context)

        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    # -----------------------------------------------------
    #                ADMIN EMAIL
    # -----------------------------------------------------
    def send_admin_email(self, subject, template_name):
        context = {
            "transaction": self,
            "username": self.user.username,
            "amount": self.amount,
            "transaction_id": self.id,
            "status": self.status,
        }

        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],   # Make sure this exists in settings.py
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    # -----------------------------------------------------
    #              SAVE OVERRIDE
    # -----------------------------------------------------
    def save(self, *args, **kwargs):
        send_notification = False
        old_status = None

        if self.pk:
            old = Transaction.objects.get(pk=self.pk)
            old_status = old.status

            # Only trigger emails if status has changed
            if old_status != self.status:
                send_notification = True

        super().save(*args, **kwargs)

        if send_notification:
            if self.status == "approved":
                self.send_user_email(
                    "Transaction Approved",
                    "investment/transaction_approved.html"
                )
                self.send_admin_email(
                    "Transaction Approved (Admin Notification)",
                    "investment/transaction_admin_notification.html"
                )

            elif self.status == "rejected":
                self.send_user_email(
                    "Transaction Rejected",
                    "investment/transaction_rejected.html"
                )
                self.send_admin_email(
                    "Transaction Rejected (Admin Notification)",
                    "investment/transaction_admin_notification.html"
                )

    # -----------------------------------------------------
    #              SIMPLE APPROVE / REJECT
    # -----------------------------------------------------
    def approve(self):
        if self.status == 'pending':
            self.status = 'approved'
            self.save()

    def reject(self):
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()




class Investment(models.Model):
    user_profile = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE)  # String reference to avoid circular import
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2)
    roi_accumulated = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    deposit_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    end_date = models.DateTimeField(null=True, blank=True)
    required_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Add default value

    def __str__(self):
        return f"Investment of ${self.deposit_amount} by {self.user_profile.user.username}"

    def save(self, *args, **kwargs):
        # Ensure deposit amount does not exceed the plan's maximum investment
        if self.plan.maximum_investment and self.deposit_amount > self.plan.maximum_investment:
            raise ValueError(f"Deposit amount exceeds the maximum allowed for this plan: {self.plan.maximum_investment}")

        # Set the end date for the investment based on the duration in days
        if not self.end_date:
            self.end_date = self.deposit_time + timedelta(days=self.plan.duration_days)

            # Ensure end_date is a datetime object (not just a date)
            if isinstance(self.end_date, datetime):  # Check if it's a datetime object
                # Ensure end_date is timezone-aware
                self.end_date = timezone.make_aware(self.end_date, timezone.get_current_timezone())
            else:
                # If it's a date object, convert to datetime
                self.end_date = timezone.make_aware(datetime.combine(self.end_date, datetime.min.time()), timezone.get_current_timezone())

        # Ensure `required_deposit` is set from the plan if not already set
        if self.required_deposit is None:
            self.required_deposit = self.plan.required_deposit or Decimal('0.00')

        # Save the instance
        super().save(*args, **kwargs)

        # Update user balance and ROI
        self.user_profile.update_balance(self.deposit_amount, 'deposit')
        self.user_profile.calculate_return_of_investment(self.deposit_amount)

    def calculate_roi(self):
        # Check if investment has expired
        if self.end_date and timezone.now() >= self.end_date:
            self.is_active = False
            self.save()
            return self.roi_accumulated  # No further ROI calculation if expired

        time_elapsed = timezone.now() - self.deposit_time
        days_elapsed = time_elapsed.days

        roi_per_day = self.deposit_amount * (self.plan.interest_rate / Decimal('100')) / Decimal('365')  # Daily ROI
        return roi_per_day * days_elapsed  # Return the accumulated ROI

    def update_roi(self):
        # Update the accumulated ROI
        new_roi = self.calculate_roi()
        self.roi_accumulated = new_roi
        self.save()

    def is_expired(self):
        return self.end_date and timezone.now() >= self.end_date






class WithdrawalRequest(models.Model):
    user_profile = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE)  # String reference to avoid circular import
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set created_at
    approved = models.BooleanField(default=False)

    def approve(self):
        if self.user_profile.balance >= self.amount:
            self.user_profile.balance -= self.amount
            self.user_profile.withdrawable_amount -= self.amount
            self.user_profile.save()

            Transaction.objects.create(
                user=self.user_profile.user,
                amount=self.amount,
                transaction_type='withdrawal',
                status='approved',
                description="Approved withdrawal"
            )

            send_mail(
                subject="Withdrawal Approved",
                message=f"Your withdrawal of ${self.amount} has been approved.",
                from_email="support@eversteadinvest.com",
                recipient_list=[self.user_profile.user.email],
            )

            self.approved = True
            self.save()
        else:
            raise ValueError("Insufficient balance to approve this withdrawal")

    def __str__(self):
        return f"Withdrawal request by {self.user_profile.user.username} for ${self.amount}"











class Wallet(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='wallet_icons/', blank=True, null=True)
    wallet_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Manage Wallets"


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UserPasswordResetForm
import logging
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from investment.models import Wallet
from userprofile.models import UserProfile
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ValidationError
import logging
from django.core.exceptions import ValidationError
from django.contrib.auth import login as django_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.models import User
from decimal import Decimal
from investment.forms import DepositForm
from .models import UserProfile
from investment.models import Wallet
from investment.forms import DepositForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from investment.forms import DepositForm
from investment.models import InvestmentPlan, Transaction, Investment
from userprofile.models import UserProfile
from django.db import transaction
from django.utils import timezone
# In userprofile/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from investment.forms import DepositForm, WithdrawalForm # Make sure you import the form from the investment app
from investment.models import Wallet, InvestmentPlan  # Adjust based on your app structure
from userprofile.models import UserProfile  # Adjust the path to your user profile model
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from investment.models import Transaction  # Import the Transaction model from the investment app
from investment.forms import DepositForm  # Assuming you already have this form in your userprofile app
from django.core.paginator import Paginator  # For pagination
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from investment.forms import WithdrawalForm
from investment.models import Wallet, Transaction, InvestmentPlan
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import UserProfileEditForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime
import logging
import logging
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from .forms import UserRegistrationForm, UserProfileForm
import logging
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from django.contrib.auth import login as django_login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from userprofile.models import UserProfile
import logging

logger = logging.getLogger(__name__)
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
import logging
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile




logger = logging.getLogger(__name__)

def register(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        messages.info(request, "You’re already logged in.")
        return redirect("userprofile:dashboard")

    initial_referral = request.GET.get("ref", "")

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Create user
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data["password1"])
                user.save()

                logger.info(f"[REGISTER] New user registered: {user.email}")

                # Create profile
                profile = profile_form.save(commit=False)
                profile.user = user

                used_ref = profile_form.cleaned_data.get("referral_bonus") or initial_referral
                if used_ref:
                    profile.used_referral_code = used_ref

                    if used_ref == "SEED14F":
                        profile.referral_reward += Decimal("50.00")
                        logger.info(f"[REFERRAL] Referral bonus applied for {user.email}")

                profile.save()

                # Send welcome email using HTML template
                try:
                    subject = "Welcome to EversteadInvest"
                    html_content = render_to_string("userprofile/register_mail.html", {
                        "username": user.username,
                        "dashboard_url": "https://www.eversteadinvest.com/userprofile/dashboard/"
                    })

                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=f"Hello {user.username}, your account has been created successfully!",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)

                    logger.info(f"[EMAIL SENT] Welcome email sent to {user.email}")

                except Exception as e:
                    logger.error(f"[EMAIL ERROR] Failed sending welcome email to {user.email}: {e}", exc_info=True)

                django_login(request, user)
                messages.success(request, "Your Wallet has been created successfully!")
                return redirect("userprofile:dashboard")

            except Exception as e:
                logger.error(f"[REGISTER ERROR] Registration failed: {e}", exc_info=True)
                messages.error(request, "Something went wrong during registration. Check logs.")
        else:
            logger.warning(f"[FORM ERROR] User form: {user_form.errors} | Profile form: {profile_form.errors}")

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm(initial={"referral_bonus": initial_referral})

    return render(request, "userprofile/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })



# @login_required
# def dashboard(request):
#     user = request.user

#     # ✅ Clear any leftover messages from previous pages (like login/register)
#     storage = messages.get_messages(request)
#     storage.used = True

#     # Ensure the UserProfile exists, if not, create one
#     try:
#         profile = user.userprofile
#     except UserProfile.DoesNotExist:
#         profile = UserProfile.objects.create(user=user)
#         messages.info(request, "Your profile has been created automatically.")

#     # Fetch all wallets from the database
#     wallets = Wallet.objects.all()

#     # Instantiate the deposit form
#     deposit_form = DepositForm()

#     # Instantiate the withdrawal form
#     withdrawal_form = WithdrawalForm()

#     # Fetch all transactions related to the user, ordered by created_at in descending order
#     transactions = Transaction.objects.filter(user=user).order_by('-created_at')
#     withdrawals = Transaction.objects.filter(user=user, transaction_type='withdrawal').order_by('-created_at')

#     # Paginate the transactions (e.g., 10 transactions per page)
#     paginator = Paginator(transactions, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Fetch all investment plans
#     investment_plans = InvestmentPlan.objects.all()

#     profile_edit_form = UserProfileEditForm(instance=profile)

#     # Render the dashboard template with the necessary context
#     return render(request, 'userprofile/dashboard.html', {
#         'user': user,
#         'profile': profile,
#         'wallets': wallets,
#         'deposit_form': deposit_form,
#         'withdrawal_form': withdrawal_form,
#         'transactions': page_obj,
#         'withdrawals': withdrawals,
#         'investment_plans': investment_plans,
#         'profile_edit_form': profile_edit_form,
#     })


@login_required
def dashboard(request):
    user = request.user

    # Clear leftover messages
    storage = messages.get_messages(request)
    storage.used = True

    # Ensure profile exists
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        messages.info(request, "Your profile has been created automatically.")

    # Fetch referrals (USERNAME ONLY)
    my_referrals = profile.get_my_referrals()

    # FIXED: Access username correctly
    referral_usernames = [ref.user.username for ref in my_referrals]

    # Wallets
    wallets = Wallet.objects.all()

    # Forms
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    # Transactions
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    withdrawals = Transaction.objects.filter(user=user, transaction_type='withdrawal').order_by('-created_at')

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Investment Plans
    investment_plans = InvestmentPlan.objects.all()

    profile_edit_form = UserProfileEditForm(instance=profile)

    return render(request, 'userprofile/dashboard.html', {
        'user': user,
        'profile': profile,
        'wallets': wallets,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': page_obj,
        'withdrawals': withdrawals,
        'investment_plans': investment_plans,
        'profile_edit_form': profile_edit_form,

        # Referrals
        'my_referrals': my_referrals,
        'referral_usernames': referral_usernames,
    })



def login(request):
    # ✅ Clear any leftover messages before showing login page
    storage = messages.get_messages(request)
    storage.used = True

    # If the user is already authenticated, redirect to the dashboard
    if request.user.is_authenticated:
        return redirect('userprofile:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Attempt to authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Log the user in
                django_login(request, user)

                # ✅ Clear any error messages before redirecting to dashboard
                storage = messages.get_messages(request)
                storage.used = True

                messages.success(request, f"Welcome back, {user.username}!")

                logger.info(f"User '{user.username}' logged in successfully.")

                return redirect('userprofile:dashboard')
            else:
                # Handle invalid credentials
                if not User.objects.filter(username=username).exists():
                    messages.error(request, "This username does not exist. Please check your username.")
                else:
                    messages.error(request, "Incorrect password. Please try again.")

                logger.error(f"Failed login attempt for username: {username}. Invalid credentials.")
        else:
            # Handle invalid form inputs
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()

    return render(request, 'userprofile/login.html', {'form': form})


logger = logging.getLogger(__name__)

def reset_password(request):
    if request.method == "POST":
        form = UserPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                # Generate reset token and email URL
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())

                reset_url = f"http://{get_current_site(request).domain}/reset/{uid}/{token}/"
                email_message = render_to_string(
                    "userprofile/password_reset_email.html",
                    {"reset_url": reset_url, "user": user}
                )

                send_mail(
                    subject="Password Reset Request",
                    message=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, "Password reset email has been sent!")
                return redirect("login")
            except User.DoesNotExist:
                # Log the error in terminal
                logger.error(f"User with email {email} does not exist.")
                messages.error(request, "Email address not found.")
                return redirect("userprofile:reset-password")

        else:
            # If the form is invalid, log the form errors in terminal
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "There was an error with your form. Please try again.")
            return render(request, "userprofile/reset_password.html", {"form": form})

    else:
        form = UserPasswordResetForm()

    return render(request, "userprofile/reset_password.html", {"form": form})









def logout(request):
    if request.user.is_authenticated:
        # Log the user out
        django_logout(request)

        # Debug: Log successful logout (optional)
        print(f"User '{request.user.username}' has logged out.")

        # Show a success message
        messages.success(request, "You have been logged out successfully.")
    else:
        # Handle the case where the user is not authenticated (optional)
        print("Attempted logout for a user who is not authenticated.")

    return redirect('userprofile:login')  # Redirect to the 'login' page using the full namespace



from investment .models import WithdrawalRequest


def recent_withdrawals(request):
    # Fetch the most recent withdrawal (ordered by the created_at date)
    most_recent_withdrawal = WithdrawalRequest.objects.filter(transaction_type='withdrawal').order_by('-created_at').first()
    context = {
        'withdrawals': [most_recent_withdrawal] if most_recent_withdrawal else []
    }
    return render(request, 'userprofile/dasboard.html', context)







@login_required
def profile_update(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            try:
                # Save the updated profile
                form.save()

                # Log the successful update
                logger.info(f"User {request.user.username}'s profile was updated successfully.")

                # Send an email to the user
                send_mail(
                    'Profile Updated Successfully',
                    f'Dear {request.user.username},\n\nYour profile has been updated successfully! We will verify your information and notify you once your profile is fully updated.',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )

                # Send an email to the admin
                send_mail(
                    'User Profile Updated',
                    f'User {request.user.username} has updated their profile.',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                # Redirect to success view
                return redirect('userprofile:profile_update_success')

            except Exception as e:
                logger.error(f"Error updating profile for {request.user.username}: {str(e)}")
                messages.error(request, "There was an error while updating your profile. Please try again.")
                return redirect('userprofile:profile_update_error')

        else:
            # Form validation failed
            logger.error(f"Profile update failed for {request.user.username}. Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
            return render(request, 'userprofile/dashboard.html', {'profile_edit_form': form})

    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'userprofile/dashboard.html', {'profile_edit_form': form})


# Success view for profile update
def profile_update_success(request):
    username = request.user.username
    return render(request, 'userprofile/kyc_success.html', {'username': username})


# Error view for profile update failure
def profile_update_error(request):
    return render(request, 'userprofile/kyc_error.html')






@login_required
def transaction_statement(request):
    # Get the logged-in user
    user = request.user

    # Fetch all transactions related to the user, ordered by created_at in descending order (most recent first)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')

    # Render the transaction statement page with the necessary context
    return render(request, 'userprofile/transaction_statement.html', {
        'user': user,
        'transactions': transactions  # Pass the transactions to the template
    })
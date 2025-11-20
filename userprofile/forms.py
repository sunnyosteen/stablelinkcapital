from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import PasswordResetForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password",
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password",
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure 'username' and 'email' fields are required
        self.fields['username'].required = True
        self.fields['email'].required = True

        # Add placeholders to username and email fields
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Phone Number"
    )
    country = CountryField(
        blank_label='Select Country'
    ).formfield(
        required=True,
        label="Country"
    )
    referral_bonus = forms.CharField(
        max_length=20,
        required=False,
        label="Referral Code"
    )
    referral_code = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.HiddenInput(),  # hidden so it won’t show in HTML
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'country', 'referral_bonus', 'referral_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields required except referral fields
        self.fields['phone_number'].required = True
        self.fields['country'].required = True
        self.fields['referral_bonus'].required = False
        self.fields['referral_code'].required = False

        # Add placeholders
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['country'].widget.attrs['placeholder'] = 'Select your country'
        self.fields['referral_bonus'].widget.attrs['placeholder'] = 'Enter referral code'

    def save(self, commit=True):
        """Ensure referral_bonus gets stored into referral_code."""
        instance = super().save(commit=False)
        referral_bonus = self.cleaned_data.get('referral_bonus')

        # Map referral_bonus → referral_code
        if referral_bonus:
            instance.referral_code = referral_bonus

        if commit:
            instance.save()
        return instance



class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        required=True,
        label="Password"
    )




class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, label="Email")




class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'govt_issued_id', 'trading_certificates', 'country', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'govt_issued_id': forms.ClearableFileInput(attrs={'multiple': False}),
            'trading_certificates': forms.ClearableFileInput(attrs={'multiple': False}),
            'country': CountrySelectWidget(attrs={'placeholder': 'Select your country'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 3}),
        }

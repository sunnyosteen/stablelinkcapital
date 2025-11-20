
from django import forms
from decimal import Decimal
from .models import InvestmentPlan
from django.core.exceptions import ValidationError

# DEPOSIT FORM

class DepositForm(forms.Form):
    selected_investment_plan = forms.ChoiceField(choices=[], required=True,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))
    amountDeposit = forms.DecimalField(max_digits=15, decimal_places=2, required=True, min_value=0.01,
                                      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Deposit'}))
    coinName = forms.CharField(max_length=255, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coin Name'}))
    paymentDate = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Payment Date'}))
    wallet_address = forms.CharField(max_length=255, required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wallet Address'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_investment_plan'].choices = [
            (plan.id, f"{plan.name} - {plan.interest_rate}% ROI for {plan.duration_days} days")
            for plan in InvestmentPlan.objects.all()
        ]

    def clean_amountDeposit(self):
        amount = self.cleaned_data['amountDeposit']
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount

    def clean_wallet_address(self):
        wallet_address = self.cleaned_data['wallet_address']
        if len(wallet_address) < 10:
            raise forms.ValidationError("Wallet address is too short.")
        return wallet_address

    def clean(self):
        cleaned_data = super().clean()

        # Retrieve the selected investment plan ID and amount to deposit
        amountDeposit = cleaned_data.get("amountDeposit")
        selected_investment_plan_id = cleaned_data.get("selected_investment_plan")

        if selected_investment_plan_id:
            try:
                selected_investment_plan = InvestmentPlan.objects.get(id=selected_investment_plan_id)
                cleaned_data['selected_investment_plan'] = selected_investment_plan  # Store the object
            except InvestmentPlan.DoesNotExist:
                raise forms.ValidationError("The selected investment plan does not exist.")
            
            required_deposit = selected_investment_plan.required_deposit if selected_investment_plan.required_deposit is not None else Decimal('0.00')

            if amountDeposit < required_deposit:
                raise forms.ValidationError(f"Amount to deposit must be at least {required_deposit} for this investment plan.")
        
        return cleaned_data


# WITHDRAWAL FORM

class WithdrawalForm(forms.Form):
    amountWithdraw = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount to Withdraw'})
    )
    wallet_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wallet Address'})
    )
    paymentDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Payment Date'}),
        required=False
    )


# INVESTMENT FORM

class InvestmentForm(forms.Form):
    selected_investment_plan = forms.ChoiceField(choices=[], required=True,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))
    amountDeposit = forms.DecimalField(max_digits=15, decimal_places=2, required=True, min_value=0.01,
                                      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Deposit'}))
    coinName = forms.CharField(max_length=255, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coin Name'}))
    paymentDate = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Payment Date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the choices with InvestmentPlan options
        self.fields['selected_investment_plan'].choices = [
            (plan.id, f"{plan.name} - {plan.interest_rate}% ROI for {plan.duration_days} days")
            for plan in InvestmentPlan.objects.all()
        ]

    def clean_amountDeposit(self):
        amount = self.cleaned_data['amountDeposit']
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount
    
    def clean(self):
        cleaned_data = super().clean()
        amountDeposit = cleaned_data.get("amountDeposit")
        selected_investment_plan_id = cleaned_data.get("selected_investment_plan")
        
        if selected_investment_plan_id:
            try:
                selected_plan = InvestmentPlan.objects.get(id=selected_investment_plan_id)
                cleaned_data['selected_investment_plan'] = selected_plan  # Store the object
            except InvestmentPlan.DoesNotExist:
                raise forms.ValidationError("The selected investment plan does not exist.")
            
            required_deposit = selected_plan.required_deposit if selected_plan.required_deposit is not None else Decimal('0.00')

            if amountDeposit < required_deposit:
                raise forms.ValidationError(f"Amount to deposit must be at least {required_deposit} for this investment plan.")
        return cleaned_data

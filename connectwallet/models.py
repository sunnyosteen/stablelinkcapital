from django.db import models
from django.contrib.auth.models import User

# Model to store wallet assets (name and image)
class WalletAsset(models.Model):
    name = models.CharField(max_length=100)
    wallet_image = models.ImageField(upload_to='wallet_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when object is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated every time the object is saved

    # Adding verbose_name and verbose_name_plural
    class Meta:
        verbose_name = 'Wallet Asset'  # Singular name for the model
        verbose_name_plural = 'Wallet Assets'  # Plural name for the model

    def __str__(self):
        return self.name

# Model to link a user to a wallet and store the wallet phrase
class ConnectWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    wallet = models.ForeignKey(WalletAsset, on_delete=models.CASCADE)  # Link to WalletAsset
    wallet_phrase = models.CharField(max_length=255, blank=True, null=True)  # Wallet phrase
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when object is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated every time the object is saved

    # Adding verbose_name and verbose_name_plural
    class Meta:
        verbose_name = 'Connected Wallet'  # Singular name for the model
        verbose_name_plural = 'Connected Wallets'  # Plural name for the model

    def __str__(self):
        return f"{self.user.username} - {self.wallet.name}"

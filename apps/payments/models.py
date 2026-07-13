from django.db import models


class PaymentMethod(models.Model):
    class Type(models.TextChoices):
        BANK_TRANSFER = "bank", "Bank Transfer"
        WALLET_QR = "wallet", "Wallet QR"
        OTHER = "other", "Others"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.WALLET_QR,
    )
    qr_image = models.ImageField(upload_to="payment_methods/", blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

import uuid

from django.db import models
from django.contrib.auth import get_user_model


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
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        type_display = dict(self.Type.choices).get(self.type, self.type)
        return f"{self.name} ({type_display})"


class Payment(models.Model):
    class statusChoices(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(
        "enrollments.Enrollment", on_delete=models.PROTECT, related_name="payments"
    )
    status = models.CharField(
        max_length=20,
        choices=statusChoices.choices,
        default=statusChoices.SUBMITTED,
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
    )
    receipt = models.ImageField(upload_to="receipts/", blank=False, null=False)
    rejection_message = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, null=True, blank=True
    )
    review_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status_display = dict(self.statusChoices.choices).get(self.status, self.status)
        return f"Payment {self.id} for Enrollment {self.enrollment.id} - Status: {status_display}"

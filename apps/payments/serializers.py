from rest_framework import serializers
from .models import Payment, PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "name",
            "type",
            "qr_image",
            "account_name",
            "account_number",
            "is_active",
            "instructions",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "enrollment",
            "payment_method",
            "receipt",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "enrollment",
            "status",
            "payment_method",
            "receipt",
            "rejection_message",
            "review_date",
            "created_at",
            "updated_at",
        ]


class PaymentAdminSerializer(PaymentSerializer):
    class Meta(PaymentSerializer.Meta):
        fields = PaymentSerializer.Meta.fields + [
            "reviewer",
        ]


class PaymentRejectSerializer(serializers.Serializer):
    rejection_message = serializers.CharField(required=True, allow_blank=False)

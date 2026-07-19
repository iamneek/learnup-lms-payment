from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Payment
from .serializers import (
    PaymentAdminSerializer,
    PaymentCreateSerializer,
    PaymentSerializer,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer

        if getattr(self.request.user, "is_staff", False):
            return PaymentAdminSerializer

        return PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        base_query = Payment.objects.select_related(
            "enrollment", "payment_method", "reviwer"
        )
        if getattr(user, "is_staff", False):
            return base_query
        return base_query.filter(enrollment__student=user)

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_payment(self, request, pk=None):
        pass

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_payment(self, request, pk=None):
        pass

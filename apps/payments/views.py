from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Payment
from .serializers import (
    PaymentAdminSerializer,
    PaymentCreateSerializer,
    PaymentRejectSerializer,
    PaymentSerializer,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .services import approve_payment, reject_payment
from rest_framework.response import Response


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
            "enrollment", "payment_method", "reviewer"
        )
        if getattr(user, "is_staff", False):
            return base_query
        return base_query.filter(enrollment__student=user)

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        payment = approve_payment(self.get_object(), request.user)
        serializer = PaymentAdminSerializer(payment)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        in_serializer = PaymentRejectSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        payment = reject_payment(
            self.get_object(),
            request.user,
            in_serializer.validated_data["rejection_message"],
        )
        out_serializer = PaymentAdminSerializer(payment)
        return Response(out_serializer.data, status=200)

    # TODO: Make this creation logic robust, avoid creating payments for enrollments that don't belong to the user
    # TODO: Make sure that once the enrollment is paid or rejeced, then no new payment can be created
    def perform_create(self, serializer):
        enrollment = serializer.validated_data["enrollment"]
        if enrollment.student != self.request.user:
            raise PermissionError(
                "You can only create payments for your own enrollment."
            )
        serializer.save()

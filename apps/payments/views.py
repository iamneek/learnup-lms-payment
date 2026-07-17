from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Payment


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_payment(self, request, pk=None):
        pass

    @action(detil=True, methods=["post"], url_path="reject")
    def reject_payment(self, request, pk=None):
        pass

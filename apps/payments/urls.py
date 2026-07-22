from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PaymentViewSet, PaymentMethodView

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payment")
urlpatterns = [
    path("payment-methods/", PaymentMethodView.as_view(), name="payment-methods"),
] + router.urls

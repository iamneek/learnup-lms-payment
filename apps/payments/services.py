from django.db.transaction import atomic
from django.utils import timezone
from apps.enrollments.models import Enrollment
from .models import Payment


@atomic
def approve_payment(payment, reviewer):
    payment.status = Payment.statusChoices.APPROVED
    payment.reviewer = reviewer
    payment.review_date = timezone.now()
    payment.save()

    enrollment = payment.enrollment
    enrollment.status = Enrollment.Status.ENROLLED
    enrollment.save()
    return payment


@atomic
def reject_payment(payment, reviewer, rejection_message):
    payment.status = Payment.statusChoices.REJECTED
    payment.reviewer = reviewer
    payment.review_date = timezone.now()
    payment.rejection_message = rejection_message
    payment.save()

    enrollment = payment.enrollment
    enrollment.status = Enrollment.Status.REJECTED
    enrollment.save()
    return payment

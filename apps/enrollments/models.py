import uuid

from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    class Status(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT", "Pending Payment"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        ENROLLED = "ENROLLED", "Enrolled"
        REJECTED = "REJECTED", "Rejected"

    class Meta:
        unique_together = ("student", "course")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="enrollments"
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.PROTECT, related_name="enrollments"
    )
    price_at_enrollment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_PAYMENT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.course} ({self.status})"

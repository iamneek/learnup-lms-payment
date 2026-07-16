from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from .models import Enrollment
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            from .serializers import CreateEnrollmentSerializer

            return CreateEnrollmentSerializer
        else:
            from .serializers import GetEnrollmentSerializer

            return GetEnrollmentSerializer

    def perform_create(self, serializer):
        student = self.request.user
        course = serializer.validated_data["course"]
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise ValidationError("You are already enrolled in this course.")
        serializer.save(student=student, price_at_enrollment=course.price)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

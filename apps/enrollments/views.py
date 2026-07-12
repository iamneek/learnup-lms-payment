from rest_framework.viewsets import ModelViewSet
from .models import Enrollment


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
        price_at_enrollment = serializer.validated_data["course"].price
        serializer.save(student=student, price_at_enrollment=price_at_enrollment)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

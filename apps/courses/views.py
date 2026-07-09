from rest_framework.viewsets import ModelViewSet

from apps.courses.models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAdminUser, AllowAny


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

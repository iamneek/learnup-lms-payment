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
            return [IsAdminUser()]
        return [AllowAny()]

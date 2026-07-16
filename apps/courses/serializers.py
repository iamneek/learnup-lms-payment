from rest_framework import serializers

from apps.courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image_url",
            "slug",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "slug": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "id": {"read_only": True},
        }

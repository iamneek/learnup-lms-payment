from rest_framework import serializers

from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer
from apps.enrollments.models import Enrollment


class CreateEnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field="slug", queryset=Course.objects.all()
    )

    class Meta:
        model = Enrollment
        fields = ["course"]


class GetEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "price_at_enrollment",
            "status",
            "created_at",
            "updated_at",
        ]

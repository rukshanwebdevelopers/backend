from core.serializers.base import BaseSerializer
from course.models import Course


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

from core.serializers.base import BaseSerializer
from course.models import Course
from enrollment.models import Enrollment


class EnrollmentSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class EnrollmentListSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

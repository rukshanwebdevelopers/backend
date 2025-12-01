from core.serializers.base import BaseSerializer
from course.models import Course
from subject.serializers import SubjectListSerializer
from user.serializers import TeacherListSerializer


class CourseSerializer(BaseSerializer):
    subject = SubjectListSerializer()
    teacher = TeacherListSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

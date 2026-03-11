# Create your views here.

from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import CourseOffering


class TeacherCourseOfferingViewSet(BaseViewSet):
    model = CourseOffering
    serializer_class = CourseOfferingListSerializer

    search_fields = ["year", "grade_level__name"]
    filterset_fields = []

    def get_queryset(self):
        user = self.request.user

        # Get the teacher linked to the logged-in user
        teacher = getattr(user, "teacher", None)

        if not teacher:
            return CourseOffering.objects.none()

        return self.filter_queryset(
            super()
            .get_queryset()
            .select_related('course', 'teacher', 'grade_level')
            .filter(teacher=teacher)
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

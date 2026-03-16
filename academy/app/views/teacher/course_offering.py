from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import CourseOffering


# Create your views here.
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

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

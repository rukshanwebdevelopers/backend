# Django imports
# Third party imports

from academy.app.permissions.base import allow_permission, ROLE
# Module imports
from academy.app.serializers.enrollment import  CourseOfferingEnrollmentListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Enrollment


class CourseOfferingEnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = CourseOfferingEnrollmentListSerializer

    search_fields = []
    ordering_fields = []

    def get_queryset(self):
        course_offering_id = self.kwargs.get("course_offering_id")
        return (
            self.filter_queryset(
                super().get_queryset()
                .select_related(
                    'student',
                    'student__user',
                    'student__current_grade',
                    'student__current_academic_year',
                )
                .filter(course_offering_id=course_offering_id)
            )
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

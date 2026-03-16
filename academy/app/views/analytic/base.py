from rest_framework import status
from rest_framework.response import Response

from academy.app.views.base import BaseAPIView
from academy.db.models import Student, Enrollment
from academy.db.models.enrollment import EnrollmentStatusType


# Create your views here.
class InstituteAnalyticsDataEndpoint(BaseAPIView):
    def get(self, request):
        student_count = Student.objects.all().count()
        enrollment_count = Enrollment.objects.all().count()
        active_enrollment_count = Enrollment.objects.filter(status=EnrollmentStatusType.ACTIVE).count()

        output = {
            "total_revenue": 0,
            "student_count": student_count,
            "enrollment_count": enrollment_count,
            "active_enrollment_count": active_enrollment_count,
        }

        return Response(output, status=status.HTTP_200_OK)

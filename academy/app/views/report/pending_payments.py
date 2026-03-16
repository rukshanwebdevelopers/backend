from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from academy.app.serializers.report import PendingPaymentListSerializer
from academy.app.views.base import BaseAPIView
from academy.db.models import Enrollment
from academy.db.models.enrollment import EnrollmentStatusType


class PendingPaymentsEndPoint(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        enrollments = Enrollment.objects.filter(
            is_active=True,
            status=EnrollmentStatusType.LOCKED,
        )
        serializer = PendingPaymentListSerializer(enrollments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from django.db import transaction
from rest_framework.response import Response

from core.views.base import BaseViewSet
from enrollment.models import EnrollmentPayment, EnrollmentStatusType
from enrollment.serializers import EnrollmentPaymentListSerializer, EnrollmentPaymentCreateSerializer


# Create your views here.
class EnrollmentPaymentViewSet(BaseViewSet):
    model = EnrollmentPayment
    serializer_class = EnrollmentPaymentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = EnrollmentPaymentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            enrollment_payment = serializer.save()

            enrollment = enrollment_payment.enrollment

            enrollment.last_payment_month = enrollment_payment.payment_month
            enrollment.last_payment_year = enrollment_payment.payment_year
            enrollment.status = EnrollmentStatusType.ACTIVE

            enrollment.save()

            return Response(EnrollmentPaymentListSerializer(enrollment_payment).data, status=201)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Django imports
from django.db import transaction

# Third party imports
from rest_framework.response import Response

# Module imports
from academy.app.serializers.enrollment import EnrollmentPaymentListSerializer, EnrollmentPaymentCreateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import EnrollmentPayment
from academy.db.models.enrollment import EnrollmentStatusType
from academy.app.permissions.base import allow_permission, ROLE


# Create your views here.
class EnrollmentPaymentViewSet(BaseViewSet):
    model = EnrollmentPayment
    serializer_class = EnrollmentPaymentListSerializer

    search_fields = ["enrollment__student__user__first_name", "enrollment__student__user__last_name"]
    ordering_fields = ['enrollment__student__user__first_name', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related('enrollment'))
        )

    @allow_permission([ROLE.ADMIN])
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

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

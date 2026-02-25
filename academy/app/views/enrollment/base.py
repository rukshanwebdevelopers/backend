from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.enrollment import EnrollmentListSerializer, EnrollmentWithPaymentMonthsSerializer, \
    EnrollmentSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Enrollment, EnrollmentPayment, Student, CourseOffering
from academy.db.models.enrollment import EnrollmentStatusType


# Create your views here.
class EnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = ["student__user__first_name", "student__user__last_name", "course_offering__grade_level__name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Enrollment.objects
            .select_related("student", "course_offering")
            .prefetch_related("enrollment_payments")
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EnrollmentWithPaymentMonthsSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = EnrollmentWithPaymentMonthsSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            enrollment = Enrollment.objects.filter(
                student=request.data.get("student"),
                course_offering=request.data.get("course_offering"),
            ).first()

            if enrollment:
                return Response(
                    {"course_offering": "The student already enroll to this course."},
                    status=status.HTTP_409_CONFLICT,
                )

            student = Student.objects.get(pk=request.data.get("student"))
            course_offering = CourseOffering.objects.get(pk=request.data.get("course_offering"))

            if student.current_grade != course_offering.grade_level:
                return Response(
                    {"course_offering": "Invalid course assignment."},
                    status=status.HTTP_409_CONFLICT,
                )

            serializer = EnrollmentSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(
                [serializer.errors[error][0] for error in serializer.errors],
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"slug": "The workspace with the slug already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

    def update(self, request, *args, **kwargs):
        # Get enrollment instance being updated
        enrollment = self.get_object()

        # Get the latest payment for this enrollment
        latest_payment = (
            EnrollmentPayment.objects
            .filter(enrollment=enrollment)
            .order_by("-payment_year", "-payment_month")
            .first()
        )

        # If a payment exists, update the enrollment fields
        if latest_payment:
            enrollment.last_payment_month = latest_payment.payment_month
            enrollment.last_payment_year = latest_payment.payment_year

            # Business rule: If paid → set ACTIVE
            enrollment.status = EnrollmentStatusType.ACTIVE
            enrollment.save()

        data = EnrollmentListSerializer(enrollment).data
        return Response(data, status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class EnrollmentPendingPaymentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        month = self.request.query_params.get("last_payment_month")
        year = self.request.query_params.get("last_payment_year")

        if month and year:
            month = int(month)
            year = int(year)

            queryset = queryset.filter(
                Q(last_payment_year__lt=year) |
                Q(
                    last_payment_year=year,
                    last_payment_month__lt=month
                )
            )

        return self.filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

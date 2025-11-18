from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from enrollment.models import Enrollment
from enrollment.serializers import EnrollmentListSerializer, EnrollmentSerializer


# Create your views here.
class EnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = ["course__name", "student__user__first_name", "student__user__last_name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        try:
            enrollment = Enrollment.objects.filter(
                student=request.data.get("student"),
                course=request.data.get("course"),
            ).first()

            if enrollment:
                return Response(
                    {"course": "The student already enroll to this course."},
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

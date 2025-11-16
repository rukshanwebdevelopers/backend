from rest_framework import status
from rest_framework.response import Response

from core.permissions.base import ROLE, allow_permission
from core.views.base import BaseViewSet
from user.models import Student
from user.serializers import StudentListSerializer, StudentCreateSerializer, StudentUpdateSerializer


class StudentViewSet(BaseViewSet):
    model = Student
    serializer_class = StudentListSerializer

    search_fields = ["student_number"]

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.save()

        output = StudentListSerializer(student, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs["pk"])

        serializer = StudentUpdateSerializer(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        output = StudentListSerializer(student, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

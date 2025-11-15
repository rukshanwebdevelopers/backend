from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from core.permissions.base import ROLE, allow_permission
from core.views.base import BaseViewSet
from user.models import Student
from user.serializers import StudentListSerializer, StudentSerializer


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

    def create(self, request):
        try:
            input_serializer = StudentSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            instance = input_serializer.save()

            # Use the output serializer (self.serializer_class)
            output_serializer = self.serializer_class(instance, context={"request": request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"slug": "The student with the username already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

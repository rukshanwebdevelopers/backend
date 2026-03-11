# Third party imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.serializers.teacher import TeacherListSerializer, TeacherCreateSerializer, TeacherUpdateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Teacher


class TeacherViewSet(BaseViewSet):
    model = Teacher
    serializer_class = TeacherListSerializer

    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'is_active', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related('user'))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = TeacherCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher = serializer.save()

        output = TeacherListSerializer(teacher, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(pk=kwargs["pk"])

        serializer = TeacherUpdateSerializer(
            teacher,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()

        output = TeacherListSerializer(teacher, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

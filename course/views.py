from rest_framework import status
from rest_framework.response import Response

from core.permissions.base import allow_permission, ROLE
from core.views.base import BaseViewSet
from course.models import Course
from course.serializers import CourseListSerializer, CourseSerializer


# Create your views here.
class CourseViewSet(BaseViewSet):
    model = Course
    serializer_class = CourseListSerializer

    search_fields = ["name", "slug"]
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = serializer.save()

        output = CourseListSerializer(course, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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

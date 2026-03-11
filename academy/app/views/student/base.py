# Third party imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.serializers.enrollment import EnrollmentListSerializer
from academy.app.serializers.student import StudentListSerializer, StudentCreateSerializer, StudentUpdateSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Student, Enrollment, CourseOffering


class StudentViewSet(BaseViewSet):
    model = Student
    serializer_class = StudentListSerializer

    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(
                super().get_queryset().select_related('user', 'current_grade', 'current_academic_year'))
        )

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def create(self, request, *args, **kwargs):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.save()

        output = StudentListSerializer(student, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
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

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StudentEnrolledCoursesEndpoint(BaseAPIView):
    def get(self, request, pk):
        student = Student.objects.get(pk=pk)

        # Get all course_offerings the student is enrolled in
        course_offerings = CourseOffering.objects.filter(enrollments__student=student)

        output = CourseOfferingListSerializer(course_offerings, many=True).data
        return Response(output, status=status.HTTP_200_OK)


class StudentMeEnrollmentsEndpoint(BaseAPIView):
    def get(self, request):
        user = request.user

        student = Student.objects.get(user=user)

        # Get all courses the student is enrolled in
        enrollments = Enrollment.objects.filter(student=student)

        output = EnrollmentListSerializer(enrollments, many=True).data
        return Response(output, status=status.HTTP_200_OK)


class StudentEnrollmentsEndpoint(BaseAPIView):
    def get(self, request, pk):
        enrollments = Enrollment.objects.filter(student_id=pk)

        output = EnrollmentListSerializer(enrollments, many=True).data
        return Response(output, status=status.HTTP_200_OK)

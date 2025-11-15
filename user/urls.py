from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views.academic_year import AcademicYearViewSet
from user.views.admin import AdminViewSet
from user.views.grade_level import GradeLevelViewSet
from user.views.student import StudentViewSet
from user.views.teacher import TeacherViewSet
from user.views.user import UserViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "admin/list/",
        AdminViewSet.as_view({"get": "list"}),
        name="admin",
    ),
    path(
        "teacher/list/",
        TeacherViewSet.as_view({"get": "list"}),
        name="teacher",
    ),
    path(
        "students/",
        StudentViewSet.as_view({"get": "list", "post": "create"}),
        name="student",
    ),
    path(
        "students/<uuid:pk>/",
        StudentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="student",
    ),
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user",
    ),
    path(
        "users/<uuid:pk>/",
        UserViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="user",
    ),
    path(
        "academicYear/",
        AcademicYearViewSet.as_view({"get": "list", "post": "create"}),
        name="academicYear",
    ),
    path(
        "academicYear/<uuid:pk>/",
        AcademicYearViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="academicYear",
    ),
    path(
        "gradeLevel/",
        GradeLevelViewSet.as_view({"get": "list", "post": "create"}),
        name="gradeLevel",
    ),
    path(
        "gradeLevel/<uuid:pk>/",
        GradeLevelViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="gradeLevel",
    ),
]

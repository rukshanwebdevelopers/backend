from django.urls import include, path
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet
from enrollment.views import EnrollmentViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        "enrollments/",
        EnrollmentViewSet.as_view({"get": "list", "post": "create"}),
        name="enrollment",
    ),
    path(
        "enrollments/<uuid:pk>/",
        EnrollmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="enrollment",
    ),
]

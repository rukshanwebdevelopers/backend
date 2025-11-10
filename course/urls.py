from django.urls import include, path
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        "courses/",
        CourseViewSet.as_view({"get": "list", "post": "create"}),
        name="course",
    ),
    path(
        "courses/<str:slug>/",
        CourseViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="course",
    ),
]

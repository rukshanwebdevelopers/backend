from django.urls import include, path
from rest_framework.routers import DefaultRouter

from subject.views import SubjectViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        "subjects/",
        SubjectViewSet.as_view({"get": "list", "post": "create"}),
        name="subject",
    ),
    path(
        "subjects/<str:slug>/",
        SubjectViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="subject",
    ),
]

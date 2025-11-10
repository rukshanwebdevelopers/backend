from django.urls import include, path
from rest_framework.routers import DefaultRouter

from guardian.views import GuardianViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        "guardians/",
        GuardianViewSet.as_view({"get": "list", "post": "create"}),
        name="guardian",
    ),
    path(
        "guardians/<str:slug>/",
        GuardianViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="guardian",
    ),
]

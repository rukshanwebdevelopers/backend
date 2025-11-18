from django.urls import include, path
from rest_framework.routers import DefaultRouter

from enrollment.views.enrollment import EnrollmentViewSet
from enrollment.views.enrollment_payment import EnrollmentPaymentViewSet

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
    path(
        "enrollment-payments/",
        EnrollmentPaymentViewSet.as_view({"get": "list", "post": "create"}),
        name="enrollment-payment",
    ),
    path(
        "enrollment-payments/<uuid:pk>/",
        EnrollmentPaymentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="enrollment-payment",
    ),
]

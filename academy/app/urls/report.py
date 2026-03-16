from django.urls import path

from academy.app.views.report.pending_payments import PendingPaymentsEndPoint

urlpatterns = [
    path(
        "reports/pending-payments/",
        PendingPaymentsEndPoint.as_view(),
        name="reports-pending-payments",
    ),
]

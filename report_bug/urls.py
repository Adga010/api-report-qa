from django.urls import path
from .views import (
    BugReportListCreateView,
    BugReportRetrieveUpdateView,
    BugReportFileUploadView,
    BugReportRetrieveDeleteView,
)

urlpatterns = [
    path(
        "/register", BugReportListCreateView.as_view(), name="bug-reports-list-create"
    ),
    path(
        "/<uuid:id>",
        BugReportRetrieveUpdateView.as_view(),
        name="bug-report-retrieve-update",
    ),
    path(
        "/upload-bug-reports",
        BugReportFileUploadView.as_view(),
        name="upload-bug-reports",
    ),
        path(
        "/<uuid:id>/",
        BugReportRetrieveDeleteView.as_view(),
        name="bug-report-detail",
    ),
]

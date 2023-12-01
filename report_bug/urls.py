from django.urls import path
from .views import (
    BugReportListCreateView,
    BugReportRetrieveUpdateView,
    BugReportFileUploadView,
    BugReportRetrieveDeleteView,
    download_bug_reports,
    get_bug_reports,
)

urlpatterns = [
    path(
        "/register/", BugReportListCreateView.as_view(), name="bug-reports-list-create"
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
    path("/download-bug-reports/", download_bug_reports, name="download-bug-reports"),
    path("/get-bug-reports/", get_bug_reports, name="get-bug-reports"),
]

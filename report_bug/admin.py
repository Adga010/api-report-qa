from django.contrib import admin
from report_bug.models import BugReport


class BugReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "STATUS",
        "PROJECT_NAME",
        "BUG",
        "CAUSAL",
        "SEVERIDAD",
        "ENLACE",
        "ENCARGADO",
        "REPORTADO",
    )


admin.site.register(BugReport)

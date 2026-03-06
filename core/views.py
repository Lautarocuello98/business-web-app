from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone

from clients.models import Client
from jobs.models import Job


def home(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    today = timezone.localdate()
    next_week = today + timedelta(days=7)

    total_clients = Client.objects.count()
    total_jobs = Job.objects.count()
    pending_jobs = Job.objects.exclude(status=Job.Status.COMPLETED).count()
    completed_jobs = Job.objects.filter(status=Job.Status.COMPLETED).count()

    upcoming_deadlines = (
        Job.objects.select_related("client")
        .filter(due_date__range=(today, next_week))
        .exclude(status=Job.Status.COMPLETED)
        .order_by("due_date")[:6]
    )

    status_labels = dict(Job.Status.choices)
    jobs_by_status = (
        Job.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )
    jobs_by_status = [
        {"label": status_labels.get(item["status"], item["status"]), "total": item["total"]}
        for item in jobs_by_status
    ]

    context = {
        "total_clients": total_clients,
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "completed_jobs": completed_jobs,
        "upcoming_deadlines": upcoming_deadlines,
        "jobs_by_status": jobs_by_status,
    }
    return render(request, "core/dashboard.html", context)


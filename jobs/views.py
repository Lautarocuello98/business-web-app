import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from clients.models import Client

from .forms import JobForm
from .models import Job


def _apply_job_filters(queryset, params):
    query = params.get("q", "").strip()
    status = params.get("status", "").strip()
    priority = params.get("priority", "").strip()
    client = params.get("client", "").strip()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(client__name__icontains=query)
            | Q(client__company__icontains=query)
        )

    valid_statuses = {choice[0] for choice in Job.Status.choices}
    if status in valid_statuses:
        queryset = queryset.filter(status=status)
    else:
        status = ""

    valid_priorities = {choice[0] for choice in Job.Priority.choices}
    if priority in valid_priorities:
        queryset = queryset.filter(priority=priority)
    else:
        priority = ""

    if client.isdigit():
        queryset = queryset.filter(client_id=int(client))
    else:
        client = ""

    filters = {
        "q": query,
        "status": status,
        "priority": priority,
        "client": client,
    }
    return queryset, filters


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.select_related("client")
        queryset, self.filters = _apply_job_filters(queryset, self.request.GET)
        return queryset.order_by("due_date", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "status_choices": Job.Status.choices,
                "priority_choices": Job.Priority.choices,
                "clients": Client.objects.order_by("name"),
                "q": self.filters["q"],
                "status": self.filters["status"],
                "priority": self.filters["priority"],
                "selected_client": self.filters["client"],
                "today": timezone.localdate(),
            }
        )
        return context


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:job_list")

    def form_valid(self, form):
        messages.success(self.request, "Job created successfully.")
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:job_list")

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully.")
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    context_object_name = "job"
    success_url = reverse_lazy("jobs:job_list")

    def form_valid(self, form):
        messages.success(self.request, "Job deleted successfully.")
        return super().form_valid(form)


@login_required
def export_jobs_csv(request):
    queryset = Job.objects.select_related("client")
    queryset, _ = _apply_job_filters(queryset, request.GET)
    queryset = queryset.order_by("due_date", "-created_at")

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="jobs_{timestamp}.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Title", "Client", "Status", "Priority", "Due Date", "Created At", "Description"]
    )
    for job in queryset:
        writer.writerow(
            [
                job.title,
                job.client.name,
                job.get_status_display(),
                job.get_priority_display(),
                job.due_date.strftime("%Y-%m-%d") if job.due_date else "",
                job.created_at.strftime("%Y-%m-%d %H:%M"),
                job.description,
            ]
        )
    return response


import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClientForm
from .models import Client


def _apply_client_search(queryset, query):
    query = query.strip()
    if not query:
        return queryset
    return queryset.filter(
        Q(name__icontains=query)
        | Q(company__icontains=query)
        | Q(email__icontains=query)
        | Q(phone__icontains=query)
    )


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10

    def get_queryset(self):
        queryset = Client.objects.all()
        self.query = self.request.GET.get("q", "").strip()
        return _apply_client_search(queryset, self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.query
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_jobs"] = self.object.jobs.order_by("-created_at")[:10]
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        messages.success(self.request, "Client created successfully.")
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        messages.success(self.request, "Client updated successfully.")
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        messages.success(self.request, "Client deleted successfully.")
        return super().form_valid(form)


@login_required
def export_clients_csv(request):
    queryset = Client.objects.all().order_by("name")
    query = request.GET.get("q", "").strip()
    queryset = _apply_client_search(queryset, query)

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="clients_{timestamp}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Company", "Email", "Phone", "Created At"])
    for client in queryset:
        writer.writerow(
            [
                client.name,
                client.company,
                client.email,
                client.phone,
                client.created_at.strftime("%Y-%m-%d %H:%M"),
            ]
        )
    return response


from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="client_list"),
    path("new/", views.ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("<int:pk>/edit/", views.ClientUpdateView.as_view(), name="client_update"),
    path("<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete"),
    path("export/csv/", views.export_clients_csv, name="client_export_csv"),
]


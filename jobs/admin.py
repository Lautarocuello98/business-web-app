from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "priority", "due_date", "created_at")
    list_filter = ("status", "priority", "due_date")
    search_fields = ("title", "description", "client__name", "client__company")
    autocomplete_fields = ("client",)
    ordering = ("due_date", "-created_at")


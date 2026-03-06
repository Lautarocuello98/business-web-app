from django.db import models
from django.utils import timezone

from clients.models import Client


class Job(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        ON_HOLD = "on_hold", "On Hold"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=180)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )
    due_date = models.DateField(blank=True, null=True, db_index=True)
    description = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        if self.status == self.Status.COMPLETED:
            return False
        return self.due_date < timezone.localdate()


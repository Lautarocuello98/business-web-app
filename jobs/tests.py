from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clients.models import Client

from .models import Job


class JobModelTests(TestCase):
    def setUp(self):
        self.business_client = Client.objects.create(name="Acme")

    def test_job_is_overdue_when_due_date_passed(self):
        job = Job.objects.create(
            client=self.business_client,
            title="Past due",
            due_date=timezone.localdate() - timedelta(days=1),
            status=Job.Status.PENDING,
        )
        self.assertTrue(job.is_overdue)

    def test_job_is_not_overdue_when_completed(self):
        job = Job.objects.create(
            client=self.business_client,
            title="Completed",
            due_date=timezone.localdate() - timedelta(days=1),
            status=Job.Status.COMPLETED,
        )
        self.assertFalse(job.is_overdue)


class JobListViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="safe-pass-123",
        )
        self.business_client = Client.objects.create(name="Acme")
        Job.objects.create(
            client=self.business_client,
            title="Pending Job",
            status=Job.Status.PENDING,
            priority=Job.Priority.MEDIUM,
        )
        Job.objects.create(
            client=self.business_client,
            title="Completed Job",
            status=Job.Status.COMPLETED,
            priority=Job.Priority.HIGH,
        )

    def test_job_list_requires_login(self):
        response = self.client.get(reverse("jobs:job_list"))
        self.assertEqual(response.status_code, 302)

    def test_can_filter_jobs_by_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("jobs:job_list"), {"status": Job.Status.COMPLETED})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Completed Job")
        self.assertNotContains(response, "Pending Job")


from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "client",
            "status",
            "priority",
            "due_date",
            "description",
            "internal_notes",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "internal_notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


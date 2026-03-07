# Business Workflow Manager

> Professional internal business workflow web app built with Django, Bootstrap, and SQLite.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Django 5](https://img.shields.io/badge/django-5.x-0c4b33.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

# Overview

Business Workflow Manager is a lightweight internal platform to manage:

- client records
- operational jobs/tasks
- priorities and status tracking
- due dates and internal notes
- dashboard metrics for decision support

The project is designed as a clean portfolio-ready Django application with authentication, protected routes, and practical business CRUD flows.

---

# Features

| Feature | Description |
|-------|-------------|
| Authentication | Login/logout with protected views |
| Dashboard Metrics | Total clients, total jobs, pending/completed jobs, upcoming deadlines, jobs by status |
| Client Management | Full CRUD for clients with search and pagination |
| Job Management | Full CRUD for jobs with status/priority and due dates |
| Advanced Job Filters | Filter by text, status, priority, and client |
| CSV Export | Export clients and jobs list views to CSV |
| Overdue Highlighting | Visual alert for overdue non-completed jobs |
| Admin Console | Django admin with search, filters, and autocomplete |

---

# Architecture

```text
business-web-app/
|-- config/                          # Project settings and root routing
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|
|-- core/                            # Home and dashboard
|   |-- __init__.py
|   |-- apps.py
|   |-- urls.py
|   |-- views.py
|   `-- templates/
|       `-- core/
|           |-- dashboard.html
|           `-- home.html
|
|-- clients/                         # Client domain
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- tests.py
|   |-- migrations/
|   |   |-- 0001_initial.py
|   |   `-- __init__.py
|   `-- templates/
|       `-- clients/
|           |-- client_confirm_delete.html
|           |-- client_detail.html
|           |-- client_form.html
|           `-- client_list.html
|
|-- jobs/                            # Job/task domain
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- tests.py
|   |-- migrations/
|   |   |-- 0001_initial.py
|   |   `-- __init__.py
|   `-- templates/
|       `-- jobs/
|           |-- job_confirm_delete.html
|           |-- job_detail.html
|           |-- job_form.html
|           `-- job_list.html
|
|-- users/                           # Authentication routes/forms
|   |-- __init__.py
|   |-- apps.py
|   |-- forms.py
|   |-- urls.py
|   `-- templates/
|       `-- registration/
|           |-- logged_out.html
|           `-- login.html
|
|-- templates/
|   `-- base.html                    # Shared layout and navbar
|
|-- static/
|   |-- css/
|   |   `-- styles.css
|   `-- js/
|       `-- app.js
|
|-- .gitignore
|-- LICENSE
|-- manage.py
|-- README.md
`-- requirements.txt
```

---

# Access Model

The app currently uses Django standard access levels:

- Anonymous user: home + login only
- Authenticated user: dashboard + clients + jobs modules
- Admin (`is_staff`/`superuser`): Django admin panel access

---

# Setup

1. Clone repository:

```bash
git clone https://github.com/Lautarocuello98/business-web-app.git
cd business-web-app
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create admin user:

```bash
python manage.py createsuperuser
```

6. Start development server:

```bash
python manage.py runserver
```

---

# App Routes

- Home: `/`
- Dashboard: `/dashboard/`
- Clients: `/clients/`
- Jobs: `/jobs/`
- Login: `/users/login/`
- Logout: `/users/logout/`
- Admin: `/admin/`

---

# Quality Checks

Current automated checks used in this repository:

```bash
python manage.py check
python manage.py test
```

Latest local run result:

- `System check identified no issues (0 silenced).`
- `Ran 7 tests ... OK`

---

# Tech Stack

- Python 3.10+
- Django 5.x
- SQLite (dev database)
- Bootstrap 5
- HTML/CSS + Django Templates

---

# Author

**Lautaro Cuello**

GitHub:
https://github.com/Lautarocuello98

---

# License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

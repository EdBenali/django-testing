# Django Learning Project

A hands-on Django sandbox managed with [Poetry](https://python-poetry.org/).

## Prerequisites

- Python 3.12+
- Poetry (`brew install poetry`)

## Setup

```bash
cd django-testing
cp .env.example .env
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser   # optional, for admin practice
poetry run python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the home page and [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) for the admin site.

## Project layout

```
django-testing/
├── config/              # Project settings, root URLs, WSGI/ASGI
├── pages/               # Starter app — add views, models, and tests here
├── templates/           # Project-wide templates (base.html)
├── static/              # Project-wide static files
├── manage.py
└── pyproject.toml       # Dependencies and Poetry config
```

## Useful commands

| Command | Purpose |
| --- | --- |
| `poetry run python manage.py runserver` | Start the dev server |
| `poetry run python manage.py makemigrations` | Create migrations from model changes |
| `poetry run python manage.py migrate` | Apply migrations |
| `poetry run python manage.py shell` | Interactive Django shell (IPython enabled) |
| `poetry run python manage.py test` | Run tests |
| `poetry run ruff check .` | Lint Python code |

## Dev tools included

- **django-debug-toolbar** — inspect SQL, templates, and requests at `/__debug__/`
- **ipython** — richer shell when you run `manage.py shell`
- **ruff** — fast Python linter

## Suggested next steps

1. Add a `Note` model in `pages/models.py` and register it in the admin.
2. Build a list/detail view for notes using function views, then refactor to class-based views.
3. Add a form for creating notes and handle POST requests.
4. Write tests in `pages/tests.py` for your views and models.

The [official Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) is an excellent companion to this project.

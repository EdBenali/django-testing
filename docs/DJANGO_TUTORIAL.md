# Django Official Tutorial — Learning Guide

Companion to the [Writing your first Django app](https://docs.djangoproject.com/en/stable/intro/tutorial01/) tutorial (Parts 1–7). Use this doc to track what each section teaches and where that work lives in **this** project.

## How this project maps to the tutorial

The tutorial builds a **polls** app inside a **mysite** project. This repo uses different names but the same patterns:

| Tutorial | This project | Notes |
| --- | --- | --- |
| `mysite/` | [`config/`](../config/) | Project package: settings, root URLs, WSGI/ASGI |
| `polls/` | [`pages/`](../pages/) | Starter app — follow the tutorial here (or add a separate `polls` app if you prefer) |
| `djangotutorial/templates/` | [`templates/`](../templates/) | Project-wide templates |
| `polls/static/polls/` | [`static/`](../static/) | Project-wide static files (tutorial uses per-app static) |

**Commands in this project** use Poetry:

```bash
poetry run python manage.py <command>
```

---

## Part 1 — Project setup, dev server, first view

**Tutorial:** [Part 1](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

### Creating a project

**Teaches:** What `django-admin startproject` generates; difference between a **project** (configuration) and an **app** (feature).

| File | Role |
| --- | --- |
| [`manage.py`](../manage.py) | CLI entry point; sets `DJANGO_SETTINGS_MODULE` |
| [`config/`](../config/) | Project Python package |
| [`config/settings.py`](../config/settings.py) | Database, installed apps, middleware, templates, etc. |
| [`config/urls.py`](../config/urls.py) | Root URLconf — “table of contents” for the site |
| [`config/wsgi.py`](../config/wsgi.py) | WSGI entry point for production servers |
| [`config/asgi.py`](../config/asgi.py) | ASGI entry point |

**Already in place.** Extra in this project: env-based settings via [`python-dotenv`](../pyproject.toml) and [`.env.example`](../.env.example).

### The development server

**Teaches:** `runserver`, auto-reload on code changes, dev server is not for production.

```bash
poetry run python manage.py runserver
```

**Try:** Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — you should see the home page, not Django’s default “Congratulations!” rocket page (this project already has a custom view).

### Creating the Polls app

**Teaches:** `startapp` layout; apps are pluggable and reusable.

| File | Status |
| --- | --- |
| [`pages/__init__.py`](../pages/) | Exists (tutorial: `polls/`) |
| [`pages/admin.py`](../pages/admin.py) | Exists, empty |
| [`pages/apps.py`](../pages/apps.py) | Exists — `PagesConfig` |
| [`pages/models.py`](../pages/models.py) | Exists, empty |
| [`pages/tests.py`](../pages/tests.py) | Exists, empty |
| [`pages/views.py`](../pages/views.py) | Exists |
| [`pages/migrations/`](../pages/) | **Create when you add models** (Part 2) |

**Also done:** `pages` is listed in `INSTALLED_APPS` in [`config/settings.py`](../config/settings.py).

### Write your first view

**Teaches:**

- A **view** is a Python function that takes `request` and returns `HttpResponse` (or similar).
- Each app has its own **URLconf** (`urls.py`).
- Root URLconf uses `include()` to delegate to app URLconfs.
- `path(route, view, name=...)` wires URLs to views.
- Only `admin.site.urls` is included directly without `include()`.

| Concept | Tutorial | This project |
| --- | --- | --- |
| App URLconf | `polls/urls.py` | [`pages/urls.py`](../pages/urls.py) |
| Root URLconf | `mysite/urls.py` | [`config/urls.py`](../config/urls.py) |
| First view | `index()` → `HttpResponse` | [`home()`](../pages/views.py) → `render()` (Part 3 shortcut) |

**Already in place:**

- [`config/urls.py`](../config/urls.py) — `path("", include("pages.urls"))` and `admin/`
- [`pages/urls.py`](../pages/urls.py) — `app_name = "pages"`, `name="home"`
- [`pages/views.py`](../pages/views.py) — `home` view

**Create as you work through Part 1 (optional poll exercise):**

- Additional views (`index`, `detail`, `results`, `vote`) returning plain `HttpResponse` strings
- URL prefix like `polls/` instead of mounting at `""` — compare tutorial’s `path("polls/", include("polls.urls"))`

---

## Part 2 — Database, models, admin

**Tutorial:** [Part 2](https://docs.djangoproject.com/en/stable/intro/tutorial02/)

### Database setup

**Teaches:**

- `DATABASES` in settings (SQLite by default)
- `INSTALLED_APPS` — built-in apps and why they need migrations
- `TIME_ZONE`, `USE_TZ`
- `python manage.py migrate` — applies migrations, creates tables

| File / command | Status |
| --- | --- |
| [`config/settings.py`](../config/settings.py) — `DATABASES`, `INSTALLED_APPS`, `TIME_ZONE` | Exists |
| `db.sqlite3` | Created after first `migrate` |
| `poetry run python manage.py migrate` | Run during setup ([`README.md`](../README.md)) |

### Creating models

**Teaches:**

- Models = database schema + Python API (DRY — define once)
- `models.Model` subclasses, `Field` types (`CharField`, `DateTimeField`, `IntegerField`)
- `ForeignKey` and `on_delete`
- `max_length`, `default`, human-readable field labels

**Create in:** [`pages/models.py`](../pages/models.py)

```python
# Tutorial models — add when you reach this section
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

### Activating models

**Teaches:** Three-step workflow for schema changes:

1. Edit `models.py`
2. `makemigrations <app_label>`
3. `migrate`

Also: `sqlmigrate`, `check`, migrations are version-controlled artifacts.

**Create when models exist:**

- [`pages/migrations/0001_initial.py`](../pages/migrations/) — via `makemigrations`

```bash
poetry run python manage.py makemigrations pages
poetry run python manage.py migrate
poetry run python manage.py sqlmigrate pages 0001   # optional: inspect SQL
poetry run python manage.py check
```

### Playing with the API

**Teaches:**

- `manage.py shell` loads Django settings and models
- `Model.objects.all()`, `.filter()`, `.get()`, `.create()`, `.save()`, `.delete()`
- `__str__()` for readable objects (important for admin)
- Custom model methods (e.g. `was_published_recently()`)
- Reverse relations: `question.choice_set`
- Field lookups: `question_text__startswith`, `pub_date__year`, `question__pub_date__year`
- Use `timezone.now()` when `USE_TZ = True`

**Practice in:** shell (`poetry run python manage.py shell`)

**Add to:** [`pages/models.py`](../pages/models.py) — `__str__` methods and `was_published_recently()`

### Introducing the Django Admin

**Teaches:**

- Admin is for staff, not public visitors
- `createsuperuser` → login at `/admin/`
- `admin.site.register(Model)` exposes models in admin
- Auto-generated forms, widgets, shortcuts, history log

| Task | Status |
| --- | --- |
| Admin URL | [`config/urls.py`](../config/urls.py) — `path("admin/", ...)` |
| Admin link in UI | [`templates/base.html`](../templates/base.html) |
| Register models | **You:** [`pages/admin.py`](../pages/admin.py) |

```bash
poetry run python manage.py createsuperuser
```

---

## Part 3 — Views, templates, URL patterns

**Tutorial:** [Part 3](https://docs.djangoproject.com/en/stable/intro/tutorial03/)

### Overview

**Teaches:** Views serve pages; URLconfs map URL patterns → views. Poll app needs: index, detail, results, vote.

### Writing more views

**Teaches:**

- URL captures: `path("<int:question_id>/", ...)`
- Converters (`int`) and named groups → keyword args to views
- Request flow: root URLconf → `include()` strips prefix → app URLconf matches remainder

**Create in:** [`pages/urls.py`](../pages/urls.py), [`pages/views.py`](../pages/views.py)

Example patterns (tutorial):

```
""                          → index
"<int:question_id>/"        → detail
"<int:question_id>/results/" → results
"<int:question_id>/vote/"   → vote
```

### Write views that actually do something

**Teaches:**

- Views query the ORM: `Question.objects.order_by("-pub_date")[:5]`
- Separate design from logic with **templates**
- Template path: `pages/templates/pages/index.html` (app namespace)
- `loader.get_template()` + `context` dict + `HttpResponse`
- **Shortcut:** `render(request, template, context)` — already used in [`pages/views.py`](../pages/views.py)

| File | Status |
| --- | --- |
| [`config/settings.py`](../config/settings.py) — `TEMPLATES`, `APP_DIRS`, `DIRS` | Exists |
| [`templates/base.html`](../templates/base.html) | Exists (project-wide base — tutorial adds per-app templates later) |
| [`pages/templates/pages/home.html`](../pages/templates/pages/home.html) | Exists |
| `pages/templates/pages/index.html` | **Create** |
| `pages/templates/pages/detail.html` | **Create** |

**Template namespacing:** Use `pages/index.html`, not bare `index.html`, to avoid collisions between apps.

### Raising a 404 error

**Teaches:**

- `Question.objects.get(pk=...)` + `except DoesNotExist` → `raise Http404`
- **Shortcut:** `get_object_or_404(Model, pk=...)`
- Also: `get_list_or_404()`

**Add to:** [`pages/views.py`](../pages/views.py) — `detail` view

### Use the template system

**Teaches:**

- `{{ variable }}` and dot lookup (dict → attribute → index)
- `{% for %}`, `{% if %}`
- Related managers in templates: `question.choice_set.all`
- `forloop.counter`

**Create:** `pages/templates/pages/detail.html` with choices loop

### Removing hardcoded URLs in templates

**Teaches:** `{% url 'name' arg %}` resolves URLs by name instead of hardcoded paths.

**Requires:** `name="detail"` (etc.) in [`pages/urls.py`](../pages/urls.py)

### Namespacing URL names

**Teaches:** `app_name = "polls"` → `{% url 'polls:detail' id %}` disambiguates apps.

**Already in place:** [`pages/urls.py`](../pages/urls.py) has `app_name = "pages"` — use `{% url 'pages:home' %}` (see [`templates/base.html`](../templates/base.html)).

---

## Part 4 — Forms, POST, generic views

**Tutorial:** [Part 4](https://docs.djangoproject.com/en/stable/intro/tutorial04/)

### Write a minimal form

**Teaches:**

- HTML `<form method="post">` for data-changing actions
- `{% csrf_token %}` on POST forms to internal URLs
- `request.POST['field']` — values are strings; use POST not GET for mutations
- Handle missing/invalid input — re-render form with `error_message`
- `F("votes") + 1` for atomic DB increment
- **Post/Redirect/Get:** `HttpResponseRedirect` after successful POST
- `reverse("polls:results", args=(id,))` — avoid hardcoded URLs in views

**Create:**

- Voting form in `pages/templates/pages/detail.html`
- `vote` view in [`pages/views.py`](../pages/views.py)
- `pages/templates/pages/results.html`
- `results` view

### Use generic views

**Teaches:** Class-based views (CBVs) reduce boilerplate for common patterns.

| Generic view | Replaces | Key attributes |
| --- | --- | --- |
| `ListView` | `index` | `get_queryset()`, `template_name`, `context_object_name` |
| `DetailView` | `detail`, `results` | `model`, `template_name` |

**Notes from tutorial:**

- Detail URL uses `<int:pk>/` not `question_id` — CBV expects `pk`
- Default templates: `<app>/<model>_detail.html`, `<app>/<model>_list.html`
- Override with `template_name`
- `ListView` default context: `question_list` — override with `context_object_name`

**Refactor in:** [`pages/views.py`](../pages/views.py), [`pages/urls.py`](../pages/urls.py)

Keep `vote` as a function view (form handling stays explicit).

---

## Part 5 — Automated testing

**Tutorial:** [Part 5](https://docs.djangoproject.com/en/stable/intro/tutorial05/)

### Introducing automated testing

**Teaches:** Why tests save time, prevent regressions, document behavior, and help teams. Test-driven development vs test-after.

### Writing our first test

**Teaches:**

- Tests live in `tests.py` (or `tests/` package); methods named `test_*`
- `django.test.TestCase` — creates/destroys test database per run
- `self.assertIs`, `self.assertEqual`, etc.
- Fix `was_published_recently()` bug (future dates should return `False`)

**Create in:** [`pages/tests.py`](../pages/tests.py)

```bash
poetry run python manage.py test pages
```

### Test a view

**Teaches:**

- **Test client:** `self.client.get(url)` simulates HTTP requests
- `reverse("polls:index")` in tests
- `response.status_code`, `response.content`, `response.context`
- `assertContains`, `assertQuerySetEqual`
- Filter queryset: only published questions (`pub_date__lte=timezone.now()`)
- `DetailView.get_queryset()` override — future questions return 404

**Add to:**

- [`pages/views.py`](../pages/views.py) — `get_queryset()` on `IndexView` / `DetailView`
- [`pages/tests.py`](../pages/tests.py) — `QuestionIndexViewTests`, `QuestionDetailViewTests`, helper `create_question()`

### Testing practices

**Teaches:** One `TestCase` class per model/view; descriptive test names; redundancy in tests is OK; consider coverage and Selenium for advanced cases.

**Placeholder exists:** [`pages/tests.py`](../pages/tests.py) — replace with real tests.

---

## Part 6 — Static files

**Tutorial:** [Part 6](https://docs.djangoproject.com/en/stable/intro/tutorial06/)

### Customize your app’s look and feel

**Teaches:**

- **Static files** = CSS, JS, images (not generated by views)
- `django.contrib.staticfiles` collects files for development and deployment
- `AppDirectoriesFinder` looks in `<app>/static/` per installed app
- **Static namespacing:** `pages/static/pages/style.css` → reference as `pages/style.css`
- `{% load static %}` and `{% static 'pages/style.css' %}`

| File | Status |
| --- | --- |
| `django.contrib.staticfiles` in `INSTALLED_APPS` | [`config/settings.py`](../config/settings.py) |
| `STATIC_URL`, `STATICFILES_DIRS` | [`config/settings.py`](../config/settings.py) |
| [`static/`](../static/) | Exists (project-wide); tutorial uses `pages/static/pages/` |
| `pages/static/pages/style.css` | **Create** (or use project `static/`) |
| Link CSS in template | **Create** in `pages/templates/pages/index.html` |

### Adding a background image

**Teaches:** Relative paths between static files (not `{% static %}` inside CSS files). Changing `STATIC_URL` won’t break relative image paths in CSS.

**Create:** `pages/static/pages/images/background.png` (any image) + CSS `url("images/background.png")`

---

## Part 7 — Customizing the admin

**Tutorial:** [Part 7](https://docs.djangoproject.com/en/stable/intro/tutorial07/)

### Customize the admin form

**Teaches:**

- `ModelAdmin` class passed as second arg to `register()`
- `fields` — field order on edit form
- `fieldsets` — grouped sections with titles; `classes: ["collapse"]`

**Edit:** [`pages/admin.py`](../pages/admin.py)

### Adding related objects

**Teaches:**

- Register related model separately vs **inlines**
- `StackedInline` vs `TabularInline`
- `extra = 3` — blank related forms on parent edit page

**Edit:** [`pages/admin.py`](../pages/admin.py) — `ChoiceInline`, `inlines`

### Customize the admin change list

**Teaches:**

- `list_display` — columns on list page (fields + callable methods)
- `@admin.display(boolean=True, ordering="pub_date", description="...")` on model methods
- `list_filter` — sidebar filters (type-aware for dates)
- `search_fields` — `LIKE` search across listed fields
- Free pagination on change lists

**Edit:** [`pages/admin.py`](../pages/admin.py) and [`pages/models.py`](../pages/models.py) (`@admin.display` on `was_published_recently`)

### Customize the admin look and feel

**Teaches:**

- Admin uses Django templates — override by copying from `django/contrib/admin/templates`
- Project `TEMPLATES['DIRS']` for site-wide overrides
- Override `admin/base_site.html` for branding
- `AdminSite.site_header` is the simpler production approach
- App-specific admin templates belong in the app’s `templates/` directory

| File | Status |
| --- | --- |
| `DIRS: [BASE_DIR / "templates"]` | [`config/settings.py`](../config/settings.py) — exists |
| `templates/admin/base_site.html` | **Create** — override admin header/branding |
| `templates/admin/index.html` | **Create** (optional) — customize admin home |

Find Django’s source templates:

```bash
poetry run python -c "import django; print(django.__path__)"
```

---

## Progress checklist

Use this to track tutorial completion in this project.

### Part 1 — Views & URLs
- [x] Project scaffold (`config/`, `manage.py`)
- [x] App scaffold (`pages/`)
- [x] App registered in `INSTALLED_APPS`
- [x] App URLconf + root `include()`
- [x] Named URL + `app_name`
- [ ] Poll-style `HttpResponse` views (`index`, `detail`, `results`, `vote` stubs)
- [ ] URL parameters (`<int:question_id>/`)

### Part 2 — Models & admin basics
- [x] Database configured (SQLite)
- [x] `migrate` for built-in apps
- [ ] `Question` and `Choice` models
- [ ] `makemigrations` + `migrate` for `pages`
- [ ] `__str__` and `was_published_recently()`
- [ ] Shell ORM practice
- [ ] `createsuperuser`
- [ ] Models registered in admin

### Part 3 — Templates
- [x] `render()` shortcut
- [x] Project base template
- [x] App template (`home.html`)
- [ ] `index.html`, `detail.html` with template tags
- [ ] `get_object_or_404` / `Http404`
- [x] `{% url %}` with namespace (`pages:home`)

### Part 4 — Forms & CBVs
- [ ] POST voting form + CSRF
- [ ] `vote` and `results` views
- [ ] `HttpResponseRedirect` + `reverse()`
- [ ] Refactor to `ListView` / `DetailView`
- [ ] Change URL `<pk>` for generic views

### Part 5 — Testing
- [ ] Model tests for `was_published_recently`
- [ ] Index view tests (past/future questions)
- [ ] Detail view 404 tests
- [ ] `get_queryset()` filters unpublished content

### Part 6 — Static files
- [x] `staticfiles` app + `STATIC_URL` + `static/` directory
- [ ] App-namespaced CSS (`pages/static/pages/`)
- [ ] `{% load static %}` in templates
- [ ] Background image in CSS

### Part 7 — Admin customization
- [ ] `QuestionAdmin` with fieldsets
- [ ] `ChoiceInline` (Tabular or Stacked)
- [ ] `list_display`, `list_filter`, `search_fields`
- [ ] `@admin.display` on model method
- [ ] `templates/admin/base_site.html` override

---

## Beyond Part 7

The tutorial continues with [Part 8 — Third-party packages](https://docs.djangoproject.com/en/stable/intro/tutorial08/) (e.g. adding features from the ecosystem). This project already includes **django-debug-toolbar** ([`config/settings.py`](../config/settings.py), [`config/urls.py`](../config/urls.py)) as a head start on that topic.

---

## Quick reference — tutorial concepts → files

| Concept | Primary file(s) in this project |
| --- | --- |
| Settings & apps | [`config/settings.py`](../config/settings.py) |
| Root routing | [`config/urls.py`](../config/urls.py) |
| App routing | [`pages/urls.py`](../pages/urls.py) |
| Views | [`pages/views.py`](../pages/views.py) |
| Models & ORM | [`pages/models.py`](../pages/models.py) |
| Migrations | `pages/migrations/` *(create in Part 2)* |
| Admin | [`pages/admin.py`](../pages/admin.py) |
| Tests | [`pages/tests.py`](../pages/tests.py) |
| Project templates | [`templates/base.html`](../templates/base.html) |
| App templates | [`pages/templates/pages/`](../pages/templates/pages/) |
| Static files | [`static/`](../static/), or `pages/static/pages/` |
| Admin template overrides | `templates/admin/` *(create in Part 7)* |
| Environment secrets | [`.env.example`](../.env.example) |
| Dependencies | [`pyproject.toml`](../pyproject.toml) |

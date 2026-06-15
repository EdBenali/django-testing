from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("pages.urls")),
    path("blog/", include("blog.urls")),
    path("admin/", admin.site.urls),
]

try:
    import debug_toolbar
except ImportError:
    pass
else:
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
    ]

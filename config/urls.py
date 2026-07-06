from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Custom dashboard — the everyday content-editing UI
    path(settings.CMS_URL_PREFIX, include("dashboard.urls")),
    # Django's built-in admin — advanced fallback, not linked anywhere
    path(settings.CMS_URL_PREFIX + "advanced/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

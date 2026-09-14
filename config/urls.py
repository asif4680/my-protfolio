from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django.views.generic import RedirectView

urlpatterns = [
    # Custom CRM / Content Management System
    path(settings.CMS_URL_PREFIX, include("crm.urls")),
    # Legacy dashboard redirect for backward compatibility
    path("dashboard/asif/<path:rest>", RedirectView.as_view(url="/crm/asif/%(rest)s", permanent=False)),
    path("dashboard/asif/", RedirectView.as_view(url="/crm/asif/", permanent=False)),
    # Django's built-in admin — advanced fallback, not linked anywhere
    path(settings.CMS_URL_PREFIX + "advanced/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

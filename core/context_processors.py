from .models import SiteSettings, SocialLink


def site_globals(request):
    return {
        "site": SiteSettings.load(),
        "social_links": SocialLink.objects.filter(is_active=True),
    }

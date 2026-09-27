from django.conf import settings


def site_metadata(request):
    """Expose deployment-safe metadata to every template."""
    return {
        "site_url": settings.SITE_URL,
        "plausible_domain": settings.PLAUSIBLE_DOMAIN,
    }

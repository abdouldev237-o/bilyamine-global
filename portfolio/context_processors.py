"""
Context processors pour le portfolio.
"""

from .models import SiteSettings


def site_settings(request):
    """Rend les paramètres du site disponibles dans tous les templates."""
    try:
        settings_obj = SiteSettings.load()
    except:
        settings_obj = None
    return {
        'site_settings': settings_obj,
    }

# accounts/context_processors.py
from .models import SiteConfiguration

def site_config(request):
    try:
        config = SiteConfiguration.objects.first()  # Assuming you have a default config object
    except SiteConfiguration.DoesNotExist:
        config = None
    return {
        'site_config': config  # Make this available to templates
    }

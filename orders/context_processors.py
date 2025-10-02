from .models import AnalyticsSettings

def analytics_settings(request):
    """Make analytics settings available in templates"""
    try:
        settings = AnalyticsSettings.objects.get(pk=1)
        return {
            'analytics_enabled': settings.analytics_enabled,
            'google_analytics_id': settings.google_analytics_id,
            'google_tag_manager_id': settings.google_tag_manager_id,
            'facebook_pixel_id': settings.facebook_pixel_id,
        }
    except AnalyticsSettings.DoesNotExist:
        return {
            'analytics_enabled': False,
            'google_analytics_id': None,
            'google_tag_manager_id': None,
            'facebook_pixel_id': None,
        }

import uuid
import json
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.db import transaction
from .models import AnalyticsSettings, VisitorSession, PageView, ConversionEvent

class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to track visitor analytics"""
    
    def process_request(self, request):
        # Get or create analytics settings
        analytics_settings, created = AnalyticsSettings.objects.get_or_create(
            pk=1,
            defaults={'analytics_enabled': True}
        )
        
        if not analytics_settings.analytics_enabled:
            return
        
        # Get or create session
        session_id = request.session.get('analytics_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['analytics_session_id'] = session_id
        
        # Get visitor info
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Extract UTM parameters
        utm_params = {
            'utm_source': request.GET.get('utm_source'),
            'utm_medium': request.GET.get('utm_medium'),
            'utm_campaign': request.GET.get('utm_campaign'),
            'utm_term': request.GET.get('utm_term'),
            'utm_content': request.GET.get('utm_content'),
        }
        
        # Create or update visitor session
        visitor_session, created = VisitorSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'referrer': referrer,
                **utm_params
            }
        )
        
        if not created:
            # Update existing session
            visitor_session.last_visit = timezone.now()
            visitor_session.save()
        
        # Store session in request for later use
        request.analytics_session = visitor_session
        request.analytics_settings = analytics_settings
    
    def process_response(self, request, response):
        if hasattr(request, 'analytics_session') and hasattr(request, 'analytics_settings'):
            if request.analytics_settings.analytics_enabled:
                # Track page view
                page_url = request.build_absolute_uri()
                page_title = getattr(request, 'page_title', 'Unknown Page')
                
                PageView.objects.create(
                    session=request.analytics_session,
                    page_url=page_url,
                    page_title=page_title
                )
                
                # Update page view count
                request.analytics_session.page_views += 1
                request.analytics_session.save()
        
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

def track_conversion(request, event_type, event_value=None, event_data=None):
    """Track a conversion event"""
    if hasattr(request, 'analytics_session'):
        ConversionEvent.objects.create(
            session=request.analytics_session,
            event_type=event_type,
            event_value=event_value,
            event_data=event_data or {}
        )
        
        # Mark session as converted
        request.analytics_session.converted = True
        request.analytics_session.save()

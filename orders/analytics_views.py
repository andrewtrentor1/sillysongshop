from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import VisitorSession, PageView, ConversionEvent, Order, AnalyticsSettings

def analytics_dashboard(request):
    """Analytics dashboard for admin users"""
    
    # Check if admin is logged in (using session-based auth like other admin pages)
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    # Get date range (last 30 days by default)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Get analytics settings
    try:
        analytics_settings = AnalyticsSettings.objects.get(pk=1)
    except AnalyticsSettings.DoesNotExist:
        analytics_settings = None
    
    # Basic metrics
    total_sessions = VisitorSession.objects.filter(first_visit__gte=start_date).count()
    total_page_views = PageView.objects.filter(timestamp__gte=start_date).count()
    total_conversions = ConversionEvent.objects.filter(timestamp__gte=start_date).count()
    total_orders = Order.objects.filter(created_at__gte=start_date).count()
    
    # Conversion rate
    conversion_rate = (total_conversions / total_sessions * 100) if total_sessions > 0 else 0
    
    # Revenue
    total_revenue = ConversionEvent.objects.filter(
        event_type='payment_complete',
        timestamp__gte=start_date
    ).aggregate(total=Sum('event_value'))['total'] or 0
    
    # Top traffic sources
    traffic_sources = VisitorSession.objects.filter(
        first_visit__gte=start_date
    ).values('utm_source').annotate(
        sessions=Count('id'),
        conversions=Count('conversions', filter=Q(conversions__event_type='form_submit'))
    ).order_by('-sessions')[:10]
    
    # Top campaigns
    campaigns = VisitorSession.objects.filter(
        first_visit__gte=start_date,
        utm_campaign__isnull=False
    ).values('utm_campaign').annotate(
        sessions=Count('id'),
        conversions=Count('conversions', filter=Q(conversions__event_type='form_submit'))
    ).order_by('-sessions')[:10]
    
    # Recent conversions
    recent_conversions = ConversionEvent.objects.filter(
        timestamp__gte=start_date
    ).select_related('session').order_by('-timestamp')[:20]
    
    # Page performance
    page_performance = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('page_title').annotate(
        views=Count('id'),
        avg_time=Avg('time_on_page')
    ).order_by('-views')[:10]
    
    # Daily stats for chart
    daily_stats = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        day_sessions = VisitorSession.objects.filter(first_visit__date=date).count()
        day_conversions = ConversionEvent.objects.filter(timestamp__date=date).count()
        daily_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'sessions': day_sessions,
            'conversions': day_conversions
        })
    
    context = {
        'analytics_settings': analytics_settings,
        'total_sessions': total_sessions,
        'total_page_views': total_page_views,
        'total_conversions': total_conversions,
        'total_orders': total_orders,
        'conversion_rate': round(conversion_rate, 2),
        'total_revenue': total_revenue,
        'traffic_sources': traffic_sources,
        'campaigns': campaigns,
        'recent_conversions': recent_conversions,
        'page_performance': page_performance,
        'daily_stats': daily_stats,
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    }
    
    return render(request, 'analytics_dashboard.html', context)

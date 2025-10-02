from django.db import models
from django.utils import timezone

class AnalyticsSettings(models.Model):
    """Analytics configuration settings"""
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True, help_text="Google Analytics 4 Measurement ID (e.g., G-XXXXXXXXXX)")
    google_tag_manager_id = models.CharField(max_length=50, blank=True, null=True, help_text="Google Tag Manager Container ID (e.g., GTM-XXXXXXX)")
    facebook_pixel_id = models.CharField(max_length=50, blank=True, null=True, help_text="Facebook Pixel ID")
    analytics_enabled = models.BooleanField(default=True, help_text="Enable/disable all analytics tracking")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Analytics Settings"
        verbose_name_plural = "Analytics Settings"

    def __str__(self):
        return f"Analytics Settings (Enabled: {self.analytics_enabled})"

class VisitorSession(models.Model):
    """Track visitor sessions and page views"""
    session_id = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True, null=True)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_term = models.CharField(max_length=100, blank=True, null=True)
    utm_content = models.CharField(max_length=100, blank=True, null=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    page_views = models.PositiveIntegerField(default=0)
    converted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Visitor Session"
        verbose_name_plural = "Visitor Sessions"

    def __str__(self):
        return f"Session {self.session_id[:8]}... ({self.page_views} views)"

class PageView(models.Model):
    """Track individual page views"""
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='pageview_set')
    page_url = models.URLField()
    page_title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_on_page = models.PositiveIntegerField(default=0, help_text="Time spent on page in seconds")

    class Meta:
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"

    def __str__(self):
        return f"{self.page_title} - {self.timestamp}"

class ConversionEvent(models.Model):
    """Track conversion events (form submissions, purchases, etc.)"""
    EVENT_TYPES = [
        ('form_submit', 'Form Submission'),
        ('payment_start', 'Payment Started'),
        ('payment_complete', 'Payment Complete'),
        ('email_signup', 'Email Signup'),
    ]
    
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='conversions')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    event_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversion Event"
        verbose_name_plural = "Conversion Events"

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"

class Order(models.Model):
    OCCASIONS = [
        ("child_birthday", "Child's Birthday 🎂"),
        ("adult_birthday", "Adult Birthday 🎉"),
        ("anniversary", "Anniversary 💍"),
        ("roast", "Roast 🥳"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    occasion = models.CharField(max_length=50, choices=OCCASIONS)
    email = models.EmailField()
    status = models.CharField(max_length=20, default="pending")
    payment_status = models.CharField(max_length=20, default="pending")
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
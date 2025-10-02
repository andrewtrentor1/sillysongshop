from django.contrib import admin
from .models import Order, AnalyticsSettings, VisitorSession, PageView, ConversionEvent

@admin.register(AnalyticsSettings)
class AnalyticsSettingsAdmin(admin.ModelAdmin):
    list_display = ("analytics_enabled", "google_analytics_id", "google_tag_manager_id", "updated_at")
    fields = ("analytics_enabled", "google_analytics_id", "google_tag_manager_id", "facebook_pixel_id")
    
    def has_add_permission(self, request):
        # Only allow one analytics settings instance
        return not AnalyticsSettings.objects.exists()

@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ("session_id", "ip_address", "utm_source", "utm_campaign", "page_views", "converted", "first_visit")
    list_filter = ("converted", "utm_source", "utm_medium", "utm_campaign", "first_visit")
    search_fields = ("session_id", "ip_address", "utm_source", "utm_campaign")
    readonly_fields = ("session_id", "ip_address", "user_agent", "first_visit", "last_visit")

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("page_title", "session", "timestamp", "time_on_page")
    list_filter = ("timestamp", "page_title")
    search_fields = ("page_title", "page_url")
    readonly_fields = ("timestamp",)

@admin.register(ConversionEvent)
class ConversionEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "session", "event_value", "timestamp")
    list_filter = ("event_type", "timestamp")
    search_fields = ("event_type", "session__session_id")
    readonly_fields = ("timestamp",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "occasion", "status", "created_at")
    list_filter = ("status", "occasion")
    search_fields = ("title", "lyrics", "email")
    actions = ["mark_as_complete"]

    def mark_as_complete(self, request, queryset):
        from .utils import send_song_ready_email
        updated = queryset.update(status="complete")
        for order in queryset.filter(status="complete"):
            send_song_ready_email(order)
        self.message_user(request, f"{updated} orders marked as complete and emails sent.")
    mark_as_complete.short_description = "Mark selected orders as complete and send emails"
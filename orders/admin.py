from django.contrib import admin
from .models import Order

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
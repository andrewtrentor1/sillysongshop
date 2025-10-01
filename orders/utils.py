from django.core.mail import send_mail
from django.conf import settings
import requests

def send_song_ready_email(order):
    try:
        send_mail(
            subject="Your Silly Song is Ready 🎶",
            message=f"""Hi there! 🎤

Your silly song "{order.title}" is ready! Thanks for ordering from Silly Song Shop.

We hope it brings lots of laughs and smiles! 🎉

Best,
The Silly Song Shop Team 🎶""",
            from_email=settings.EMAIL_HOST_USER or 'Silly Notifications <noreply@sillysongshop.com>',
            recipient_list=[order.email],
            fail_silently=True,  # Don't crash if email fails
        )
        print(f"DEBUG: Email sent to {order.email} for order {order.title}")
    except Exception as e:
        print(f"DEBUG: Email failed to send: {e}")
        # Continue without crashing

def send_payment_confirmation_email(order):
    try:
        send_mail(
            subject="Payment Confirmed - Your Order is Processing! 🎵",
            message=f"""Hi there! 🎤

Great news! Your payment has been confirmed and your order is now being processed.

Order Details:
- Song Title: {order.title}
- Occasion: {order.get_occasion_display()}
- Your Details: {order.lyrics}
- Status: Processing

Our team is working on your custom song and you'll receive it via email within 1 hour!

Thanks for choosing Silly Song Shop! 🎶

Best,
The Silly Song Shop Team 🎵""",
            from_email=settings.EMAIL_HOST_USER or 'Silly Notifications <noreply@sillysongshop.com>',
            recipient_list=[order.email],
            fail_silently=True,  # Don't crash if email fails
        )
        print(f"DEBUG: Payment confirmation email sent to {order.email} for order {order.title}")
    except Exception as e:
        print(f"DEBUG: Payment confirmation email failed to send: {e}")
        # Continue without crashing

def send_discord_notification(order):
    """Send Discord notification when an order is confirmed"""
    webhook_url = "https://discord.com/api/webhooks/1423021199344140319/a__D8LMRVynNgv3pqfYxZx5PeQqeG8_mk7QrnJSMOWnu_gSxjd_gmGQbzW75a6GE-KfA"

    try:
        # Truncate lyrics if too long for Discord (field value limit is 1024 chars)
        lyrics_display = order.lyrics if len(order.lyrics) <= 1000 else order.lyrics[:1000] + "..."

        embed = {
            "embeds": [{
                "title": "🎵 New Order Confirmed!",
                "color": 5814783,  # Purple color
                "fields": [
                    {"name": "Order ID", "value": f"#{order.id}", "inline": True},
                    {"name": "Amount", "value": "$9.99", "inline": True},
                    {"name": "Payment Status", "value": order.payment_status.capitalize(), "inline": True},
                    {"name": "Song Title", "value": order.title, "inline": False},
                    {"name": "Occasion", "value": order.get_occasion_display(), "inline": True},
                    {"name": "Customer Email", "value": order.email, "inline": True},
                    {"name": "Status", "value": order.status.capitalize(), "inline": True},
                    {"name": "Order Details", "value": lyrics_display, "inline": False},
                ],
                "timestamp": order.created_at.isoformat(),
                "footer": {"text": "Silly Song Shop"}
            }]
        }

        response = requests.post(webhook_url, json=embed, timeout=10)
        response.raise_for_status()
        print(f"DEBUG: Discord notification sent for order {order.id}")
    except Exception as e:
        print(f"DEBUG: Discord notification failed: {e}")
        # Continue without crashing

from django.core.mail import send_mail
from django.conf import settings

def send_song_ready_email(order):
    try:
        send_mail(
            subject="Your Silly Song is Ready 🎶",
            message=f"""Hi there! 🎤

Your silly song "{order.title}" is ready! Thanks for ordering from Silly Song Shop.

We hope it brings lots of laughs and smiles! 🎉

Best,
The Silly Song Shop Team 🎶""",
            from_email=settings.EMAIL_HOST_USER or 'noreply@sillysongshop.com',
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
- Status: Processing

Our team is working on your custom song and you'll receive it via email within 1 hour!

Thanks for choosing Silly Song Shop! 🎶

Best,
The Silly Song Shop Team 🎵""",
            from_email=settings.EMAIL_HOST_USER or 'noreply@sillysongshop.com',
            recipient_list=[order.email],
            fail_silently=True,  # Don't crash if email fails
        )
        print(f"DEBUG: Payment confirmation email sent to {order.email} for order {order.title}")
    except Exception as e:
        print(f"DEBUG: Payment confirmation email failed to send: {e}")
        # Continue without crashing

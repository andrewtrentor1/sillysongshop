from django.core.mail import send_mail
from django.conf import settings

def send_song_ready_email(order):
    send_mail(
        subject="Your Silly Song is Ready 🎶",
        message=f"""Hi there! 🎤

Your silly song "{order.title}" is ready! Thanks for ordering from Silly Song Shop.

We hope it brings lots of laughs and smiles! 🎉

Best,
The Silly Song Shop Team 🎶""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email],
        fail_silently=False,
    )

def send_payment_confirmation_email(order):
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
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email],
        fail_silently=False,
    )

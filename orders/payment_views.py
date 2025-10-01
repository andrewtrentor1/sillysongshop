import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Order

# Set your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(request, order_id):
    """Create a Stripe payment intent for an order"""
    order = get_object_or_404(Order, id=order_id)
    
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid for!')
        return redirect('order_song')
    
    try:
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=999,  # $9.99 in cents
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                'order_id': order.id,
                'order_title': order.title,
                'customer_email': order.email
            }
        )
        
        # Update order with payment intent ID
        order.stripe_payment_intent_id = intent.id
        order.save()
        
        return render(request, 'checkout.html', {
            'order': order,
            'client_secret': intent.client_secret,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })
        
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('order_song')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks for payment confirmation"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    print(f"DEBUG: Webhook received - {request.method}")
    print(f"DEBUG: Payload length: {len(payload)}")
    
    # For now, let's skip signature verification in development
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"DEBUG: Invalid payload: {e}")
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"DEBUG: Invalid signature: {e}")
        return JsonResponse({'status': 'invalid signature'}, status=400)
    
    print(f"DEBUG: Event type: {event['type']}")
    
    # Handle successful payment
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']
        
        print(f"DEBUG: Payment succeeded for order {order_id}")
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'paid'
            order.save()
            
            print(f"DEBUG: Order {order_id} marked as paid")
            
            # Send confirmation email
            from .utils import send_payment_confirmation_email, send_discord_notification
            send_payment_confirmation_email(order)
            send_discord_notification(order)
            
        except Order.DoesNotExist:
            print(f"DEBUG: Order {order_id} not found")
    
    return JsonResponse({'status': 'success'})

def payment_success(request):
    """Show payment success page and update order status"""
    order_id = request.GET.get('order_id')
    
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            if order.payment_status == 'pending':
                order.payment_status = 'paid'
                order.save()
                print(f"DEBUG: Order {order.id} marked as paid from success page")
                
                # Send confirmation email
                from .utils import send_payment_confirmation_email, send_discord_notification
                send_payment_confirmation_email(order)
                send_discord_notification(order)
            else:
                print(f"DEBUG: Order {order.id} already paid")
        except Order.DoesNotExist:
            print(f"DEBUG: Order {order_id} not found")
        except Exception as e:
            print(f"DEBUG: Error updating order status: {e}")
    
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    """Show payment cancelled page"""
    return render(request, 'payment_cancelled.html')

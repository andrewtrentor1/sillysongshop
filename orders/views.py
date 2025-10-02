from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order
from .utils import send_song_ready_email
from .analytics_middleware import track_conversion

def order_song(request):
    if request.method == "POST":
        # Get the basic form data
        title = request.POST.get('title', '')
        occasion = request.POST.get('occasion', '')
        email = request.POST.get('email', '')
        
        print(f"DEBUG: Title: '{title}'")
        print(f"DEBUG: Occasion: '{occasion}'")
        print(f"DEBUG: Email: '{email}'")
        
        # Basic validation
        if not title or not occasion or not email:
            messages.error(request, 'Please fill in all required fields.')
            form = OrderForm()
            return render(request, "order.html", {"form": form})
        
        # Create a valid form instance for the redirect
        form = OrderForm({'title': title, 'occasion': occasion})
        if form.is_valid():
            # Get additional data from the form
            occasion = form.cleaned_data['occasion']
            title = form.cleaned_data['title']
            print(f"DEBUG: Title from form: '{title}'")
            print(f"DEBUG: Occasion from form: '{occasion}'")
            
            # Get dynamic fields based on occasion
            if occasion == 'child_birthday':
                child_name = request.POST.get('child_name', '')
                child_age = request.POST.get('child_age', '')
                child_interests = request.POST.get('child_interests', '')
                song_style = request.POST.get('song_style', '')
                other_style = request.POST.get('other_style', '')
                email = request.POST.get('email', '')
                
                # Combine all info into lyrics field
                lyrics = f"Child's Name: {child_name}\n"
                lyrics += f"Age: {child_age}\n"
                lyrics += f"Interests/Theme: {child_interests}\n"
                lyrics += f"Song Style: {song_style}"
                if other_style:
                    lyrics += f" ({other_style})"
                    
            elif occasion == 'adult_birthday':
                adult_name = request.POST.get('adult_name', '')
                adult_age = request.POST.get('adult_age', '')
                adult_interests = request.POST.get('adult_interests', '')
                song_style = request.POST.get('song_style_adult', '')
                other_style = request.POST.get('other_style_adult', '')
                email = request.POST.get('email', '')
                
                lyrics = f"Person's Name: {adult_name}\n"
                lyrics += f"Age: {adult_age}\n"
                lyrics += f"Interests/Theme: {adult_interests}\n"
                lyrics += f"Song Style: {song_style}"
                if other_style:
                    lyrics += f" ({other_style})"
                    
            elif occasion == 'anniversary':
                couple_names = request.POST.get('couple_names', '')
                years_together = request.POST.get('years_together', '')
                anniversary_details = request.POST.get('anniversary_details', '')
                song_style = request.POST.get('song_style_anniversary', '')
                other_style = request.POST.get('other_style_anniversary', '')
                email = request.POST.get('email', '')
                
                lyrics = f"Couple's Names: {couple_names}\n"
                lyrics += f"Years Together: {years_together}\n"
                lyrics += f"Details: {anniversary_details}\n"
                lyrics += f"Song Style: {song_style}"
                if other_style:
                    lyrics += f" ({other_style})"
                    
            elif occasion == 'roast':
                roast_target = request.POST.get('roast_target', '')
                roast_level = request.POST.get('roast_level', '')
                roast_topics = request.POST.get('roast_topics', '')
                song_style = request.POST.get('song_style_roast', '')
                other_style = request.POST.get('other_style_roast', '')
                email = request.POST.get('email', '')
                
                lyrics = f"Person to Roast: {roast_target}\n"
                lyrics += f"Roast Level: {roast_level}\n"
                lyrics += f"Topics: {roast_topics}\n"
                lyrics += f"Song Style: {song_style}"
                if other_style:
                    lyrics += f" ({other_style})"
                    
            else:  # other
                other_occasion = request.POST.get('other_occasion', '')
                other_recipient = request.POST.get('other_recipient', '')
                other_vibe = request.POST.get('other_vibe', '')
                other_details = request.POST.get('other_details', '')
                song_style = request.POST.get('song_style_other', '')
                other_style = request.POST.get('other_style_other', '')
                email = request.POST.get('email', '')
                
                lyrics = f"Occasion: {other_occasion}\n"
                lyrics += f"Recipient: {other_recipient}\n"
                lyrics += f"Vibe: {other_vibe}\n"
                lyrics += f"Details: {other_details}\n"
                lyrics += f"Song Style: {song_style}"
                if other_style:
                    lyrics += f" ({other_style})"
            
            # Create the order
            print(f"DEBUG: Creating order with title='{title}', email='{email}'")
            order = Order.objects.create(
                title=title,
                lyrics=lyrics,
                occasion=occasion,
                email=email,
                status='pending',
                payment_status='pending'
            )
            print(f"DEBUG: Order created successfully with ID: {order.id}")
            
            # Track conversion event
            track_conversion(
                request, 
                'form_submit', 
                event_data={
                    'order_id': order.id,
                    'occasion': occasion,
                    'title': title
                }
            )
            
            # Redirect to payment page
            return redirect('create_payment_intent', order_id=order.id)
        else:
            print(f"DEBUG: Form validation failed: {form.errors}")
            messages.error(request, 'Please check your form and try again.')
    else:
        form = OrderForm()
    return render(request, "order.html", {"form": form})

def admin_login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        if password == 'PickleKings1425':
            request.session['admin_logged_in'] = True
            # Get the next URL from the request, default to order_list
            next_url = request.GET.get('next', 'order_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid password')
    return render(request, 'admin_login.html')

def order_list(request):
    # Check if admin is logged in
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    # Get all orders
    all_orders = Order.objects.all().order_by('-created_at')
    
    # Separate orders by payment status
    paid_orders = all_orders.filter(payment_status='paid')
    unpaid_orders = all_orders.filter(payment_status='pending')
    completed_orders = all_orders.filter(status='complete')
    
    return render(request, 'order_list.html', {
        'orders': all_orders,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders,
        'completed_orders': completed_orders,
    })

def mark_complete(request, order_id):
    # Check if admin is logged in
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'complete'
        order.save()
        
        # Send email notification
        send_song_ready_email(order)
        
        messages.success(request, f'Order "{order.title}" marked as complete and email sent!')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
    
    return redirect('order_list')

def delete_order(request, order_id):
    # Check if admin is logged in
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    try:
        order = Order.objects.get(id=order_id)
        order_title = order.title
        order.delete()
        messages.success(request, f'Order "{order_title}" has been deleted successfully!')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
    
    return redirect('order_list')

def admin_logout(request):
    request.session.pop('admin_logged_in', None)
    return redirect('admin_login')
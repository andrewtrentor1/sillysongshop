"""
URL configuration for weirdsongfactory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from orders.views import order_song, admin_login, order_list, mark_complete, delete_order, admin_logout
from orders.payment_views import create_payment_intent, payment_success, payment_cancelled, stripe_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", order_song, name="order_song"),
    path("admin-login/", admin_login, name="admin_login"),
    path("orders/", order_list, name="order_list"),
    path("orders/complete/<int:order_id>/", mark_complete, name="mark_complete"),
    path("orders/delete/<int:order_id>/", delete_order, name="delete_order"),
    path("admin-logout/", admin_logout, name="admin_logout"),
    # Payment URLs
    path("checkout/<int:order_id>/", create_payment_intent, name="create_payment_intent"),
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancelled/", payment_cancelled, name="payment_cancelled"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/assets/', document_root='assets')

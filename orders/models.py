from django.db import models

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
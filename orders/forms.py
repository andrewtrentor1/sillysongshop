from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["title", "occasion"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Song title",
                "class": "form-control"
            }),
            "occasion": forms.Select(attrs={
                "class": "form-control"
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value to "Child's Birthday"
        self.fields['occasion'].initial = 'child_birthday'

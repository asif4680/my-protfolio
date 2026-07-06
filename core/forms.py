from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@company.com", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={
                "placeholder": "What is this about?"}),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell me about your project…", "rows": 6}),
        }

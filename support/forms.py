from django import forms

from .models import Tickets, Message


class TicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "موضوع تیکت"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "متن پیام شما..."}
            ),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "پاسخ خود را بنویسید...",
                }
            ),
        }

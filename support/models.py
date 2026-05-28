from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tickets(models.Model):
    class Status(models.TextChoices):
        open = "open", _("open")
        closed = "closed", _("closed")
        in_progress = "in_progress", _("in progress")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.open
    )
    description = models.TextField(max_length=1000)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tickets"
        verbose_name = "Ticket"
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"{self.title} - {self.user.first_name} {self.user.last_name}"


class Message(models.Model):
    ticket = models.ForeignKey(
        Tickets, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.first_name} {self.sender.last_name} on {self.ticket.id}"

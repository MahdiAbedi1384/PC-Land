from django.contrib import admin

from .models import Tickets, Message


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "status",
        "datetime_created",
        "datetime_updated",
    ]
    list_display_links = [
        "id",
    ]
    list_filter = [
        "status",
        "datetime_created",
        "datetime_updated",
    ]
    list_per_page = 20
    search_fields = [
        "title",
        "user__first_name",
        "user__last_name",
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ticket",
        "sender",
        "created_at",
    ]
    list_display_links = [
        "id",
    ]
    list_filter = [
        "sender",
        "created_at",
    ]
    list_per_page = 20
    search_fields = [
        "content",
    ]

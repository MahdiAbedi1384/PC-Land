from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TicketForm, MessageForm
from .models import Tickets


@login_required
def ticket_list(request):
    # ادمین همه تیکت‌ها و کاربر عادی فقط تیکت‌های خودش را می‌بیند
    if request.user.is_staff:
        tickets = Tickets.objects.all().order_by("-datetime_updated")
    else:
        tickets = Tickets.objects.filter(user=request.user).order_by(
            "-datetime_updated"
        )

    return render(request, "ticket_list.html", {"tickets": tickets})


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        form = TicketForm()

    return render(request, "create_ticket.html", {"form": form})


@login_required
def ticket_detail(request, ticket_id):
    # کاربر فقط می‌تواند تیکت خودش را باز کند (ادمین می‌تواند همه را باز کند)
    if request.user.is_staff:
        ticket = get_object_or_404(Tickets, id=ticket_id)
    else:
        ticket = get_object_or_404(Tickets, id=ticket_id, user=request.user)

    messages = ticket.messages.all()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.ticket = ticket
            new_message.sender = request.user
            new_message.save()

            # آپدیت زمان آخرین تغییر تیکت
            ticket.save()
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        form = MessageForm()

    return render(
        request,
        "ticket_detail.html",
        {"ticket": ticket, "messages": messages, "form": form},
    )

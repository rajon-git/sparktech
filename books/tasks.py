# app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Borrow
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_due_date_emails():
    today = timezone.now().date()
    borrows = Borrow.objects.filter(due_date=today, return_date__isnull=True)

    for borrow in borrows:
        send_mail(
            subject="Library Reminder: Book Return Due Today",
            message=(
                f"Dear {borrow.user.first_name or borrow.user.username},\n\n"
                f"This is a courteous reminder that the book you borrowed from our library, "
                f"**'{borrow.book.title}'**, is due for return today.\n\n"
                "Please ensure that the book is returned by the end of the day to avoid any late return penalties.\n\n"
                "Thank you for using our library services.\n\n"
                "Best regards,\n"
                "Library Management System"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[borrow.user.email],
        )

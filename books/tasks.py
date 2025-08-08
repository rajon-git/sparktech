from collections import defaultdict
from celery import shared_task
from django.utils import timezone
from .models import Borrow
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_due_date_emails():
    today = timezone.now().date()
    borrows = Borrow.objects.select_related('user', 'book').filter(
        due_date=today,
        return_date__isnull=True
    )
    user_borrow_map = defaultdict(list)
    for borrow in borrows:
        user_borrow_map[borrow.user].append(borrow.book.title)
    for user, book_titles in user_borrow_map.items():
        books_list = "\n".join(f"- {title}" for title in book_titles)
        message = (
            f"Dear {user.first_name},\n\n"
            "This is a courteous reminder that the following books you borrowed from our library are due for return today:\n\n"
            f"{books_list}\n\n"
            "Please ensure that the books are returned by the end of the day to avoid any late return penalties.\n\n"
            "Thank you for using our library services.\n\n"
            "Best regards,\n"
            "Library Management System"
        )
        send_mail(
            subject="Library Reminder: Book Returns Due Today",
            message=message, from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

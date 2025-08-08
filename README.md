Project Title: Library Management & Borrowing System

All API endpoints Postman documentation below: https://documenter.getpostman.com/view/24667147/2sB3BDLBV1

Features:
    1. User Registration and Login (JWT)
    2. Admin can manage books and view all borrow records
    3. Users can borrow and return books
    4. Penalty system for overdue returns
    5. Email reminders for due dates
    6. API rate limiting per user
    7. Asynchronous email notifications using Celery
    8. Periodic task scheduling with `django-celery-beat`

How Borrowing and Returning Logic Works:
    1. A user must be authenticated to borrow a book.
    2. Active Borrow Limit: A user cannot have more than 3 active borrowings at once.
    3. Book Availability: The selected book must have at least one available copy.
    4. A new Borrow record is created with: 
        i. borrow_date as the current date.
        ii. due_date automatically set to 14 days from the borrow date.
    5. The available_copies of the book is decreased by 1

Returning a Book:
    1. A user must be authenticated and  provide the borrow_id of the book they are returning. 
    2. That the borrow record exists and has not already been returned.
    3. Calculates whether the book is returned late.
    4. Sets the return_date to today.
    5. Increases the available_copies of the book by 1.
    6. If the book is returned late, it calculates the number of overdue days and adds them as penalty points to the user's profile (1 point per day).

How Penalty Points Are Calculated:
    1. Penalty points are only added if the book is returned after the due date.
    2. For each day past the due_date, the user earns 1 penalty point.
    3. These points are stored in the Profile model under penalty_points.
    4. Users can view their own penalties; only staff can view others

How to Run:

    1. Clone the repo.
    2. Create and activate a virtual environment.
    3. Install dependencies (pip install -r requirements.txt).
    4. In the root directory, create a .env file and edit it as shown below.
    5. Run migrations (python manage.py migrate)
    6. Celery task Configuration: 
        i. Go to the Django Admin Panel.
        ii. Log in with a superuser account.
        iii. In Periodic Tasks : 
            Create an crontabs (minutes:0, hours: 9  ; its means 9:30 am Give Due Date Email to user) , 
            Create the Periodic Task ( Name: Send email notification on due date, Task: books.tasks.send_due_date_emails,
            Crontab Schedule: You created Select this)

    7. Start Redis server (redis-server).
    8. Run Celery worker another terminal (celery -A sparktech worker --beat --loglevel=info).
    9. Start Django development server (python manage.py runserver).
    10. Done 


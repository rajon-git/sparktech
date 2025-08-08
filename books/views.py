from rest_framework import generics, permissions, status
from .models import Book, Borrow, Author, Category
from . serializers import BookSerializer, AuthorSerializer, CategorySerializer, BorrowSerializer, ReturnBookSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import UpdateAPIView
from accounts.models import Profile
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.
class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()] 

    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author')
        category_id = self.request.query_params.get('category')

        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
class BorrowListCreateView(generics.ListCreateAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user, return_date__isnull=True)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book_id')

        print(f"<-----{user}------>")
        print(f"<-----{book_id}------>")

        if not book_id:
            return Response({'error': 'book field is required'}, status=status.HTTP_400_BAD_REQUEST)

        active_borrows = Borrow.objects.filter(user=user, return_date__isnull=True).count()
        if active_borrows >= 3:
            return Response({'error': 'You have reached the borrowing limit of 3 active books.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.select_for_update().get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies < 1:
            return Response({'error': 'This book is currently not available.'}, status=status.HTTP_400_BAD_REQUEST)

        book.available_copies -= 1
        book.save()

        borrow = Borrow.objects.create(
            user=user,
            book=book,
            due_date=timezone.now().date() + timezone.timedelta(days=14)
        )

        serializer = self.get_serializer(borrow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ReturnBookView(UpdateAPIView):
    queryset = Borrow.objects.select_related('user', 'book').all()
    serializer_class = ReturnBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrow_id = request.data.get('borrow_id')

        if not borrow_id:
            return Response({"error": "borrow_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrow = self.queryset.get(id=borrow_id)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow record not found."}, status=status.HTTP_404_NOT_FOUND)

        if borrow.return_date:
            return Response({"message": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            today = timezone.now().date()
            borrow.return_date = today
            borrow.save()

            borrow.book.available_copies += 1
            borrow.book.save()

            late_days = 0
            if today > borrow.due_date:
                late_days = (today - borrow.due_date).days
                profile = Profile.objects.get(user=borrow.user)
                profile.penalty_points += late_days
                profile.save()

        return Response({
            "message": "Book returned successfully.",
            "return_date": today,
            "late_days": late_days,
            "penalty_added": late_days,
            "total_penalty_points": profile.penalty_points if late_days else 0
        }, status=status.HTTP_200_OK)
    
class UserPenaltyPointsView(APIView):
    def get_permissions(self):
        if self.request.user.is_staff:
            return [permissions.AllowAny()] 
        return [permissions.IsAuthenticated()]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        
        if request.user != user and not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'penalty_points': user.profile.penalty_points})
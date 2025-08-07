from rest_framework import generics, permissions
from .models import Book, Borrow
from . serializers import BookSerializer

# Create your views here.
class GetBookViews(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field  = 'id'

class GetBookListViews(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAdminUser]
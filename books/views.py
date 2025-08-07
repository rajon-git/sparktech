from rest_framework import generics, permissions
from .models import Book, Borrow
from . serializers import BookSerializer

# Create your views here.
class GetBookViews(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field  = 'id'

class GetBookListViews(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author')
        category_id = self.request.query_params.get('category')

        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
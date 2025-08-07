from rest_framework import serializers
from .models import Book, Author, Category, Borrow
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    author_id = serializers.PrimaryKeyRelatedField( queryset=Author.objects.all(), 
        source='author', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField( queryset=Category.objects.all(),
        source='category', write_only=True
    )

    class Meta:
        model = Book
        fields = '__all__'


class BorrowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = '__all__'



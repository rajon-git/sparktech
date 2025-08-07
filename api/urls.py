from django.urls import path 
from accounts.views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from books import views as book_views

urlpatterns = [
    path("register/",RegisterView.as_view(), name='register'),
    path("login/", TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('books/', book_views.BookListCreateView.as_view(), name='book-create-list'),
    path('books/<int:id>/', book_views.BookRetrieveUpdateDeleteView.as_view(), name='book-read-update-delete'),

    path('authors/', book_views.AuthorListCreateView.as_view(), name='authors-create-delete'),
    path('categories/', book_views.CategoryListCreateView.as_view(), name='categories-create-delete'),
] 


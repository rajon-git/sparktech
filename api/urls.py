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

    # books api
    path('books/<int:id>/', book_views.GetBookViews.as_view(), name='book_detail'),
    path('books/', book_views.GetBookListViews.as_view(), name='all_books'),
] 


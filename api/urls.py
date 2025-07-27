from django.urls import path
from .views import (RegisterView, LoginView, CompanyListAPIView, RegisterCompany,
                    CheckAuthView, WatchlistCreateOrUpdateView, WatchlistListView, RemoveStockFromWatchlistAPIView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('companies/', CompanyListAPIView.as_view(), name='companies'),
    path('addCompany/', RegisterCompany.as_view(), name='createCompany'),
    path("check-auth/", CheckAuthView.as_view(), name='checkauth'),
    path("watchlist/add/", WatchlistCreateOrUpdateView.as_view(), name='watchlist'),
    path("watchlist/", WatchlistListView.as_view()),
    path("watchlist/remove/", RemoveStockFromWatchlistAPIView.as_view())
]

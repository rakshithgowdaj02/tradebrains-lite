from django.urls import path
from .views import (RegisterView, LoginView, CompanyListAPIView, RegisterCompany,
                    CheckAuthView, WatchlistCreateOrUpdateView, WatchlistListView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('companies/', CompanyListAPIView.as_view(), name='companies'),
    path('addCompany/', RegisterCompany.as_view(), name='createCompany'),
    path("check-auth/", CheckAuthView.as_view(), name='checkauth'),
    path("createWatchlist/", WatchlistCreateOrUpdateView.as_view(), name='watchlist'),
    path("watchlist/", WatchlistListView.as_view())
]

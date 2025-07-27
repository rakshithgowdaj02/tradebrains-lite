from rest_framework import generics, filters, status
from .models import User, Company, WatchlistDetail
from .serializers import (RegisterSerializer, UserLoginSerializer, CompanySerializer,
                          CompanyRegisterSerializer, WatchlistDetailSerializer, WatchlistListDetailSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = []  # Public

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCompany(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer
    permission_classes = [IsAuthenticated]


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
        })


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sector', 'symbol']
    ordering_fields = ['name', 'sector', 'created_on']


class WatchlistCreateOrUpdateView(generics.CreateAPIView):
    serializer_class = WatchlistDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchlistDetail.objects.filter(user=self.request.user)


class WatchlistListView(generics.ListAPIView):
    serializer_class = WatchlistListDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchlistDetail.objects.filter(user=self.request.user)

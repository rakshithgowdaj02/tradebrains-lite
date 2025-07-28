from rest_framework import serializers, status
from .models import User, Company, WatchlistStockDetail, WatchlistDetail
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'mobile')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # properly hashes the password
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Must include username and password.")

        refresh = RefreshToken.for_user(user)

        return {
            'status': True,
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email
        }


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'symbol', 'scriptcode', 'created_on', 'modified_on']
        read_only_fields = ['created_on', 'modified_on']

    def validate(self, data):
        symbol = data.get('symbol')
        scriptcode = data.get('scriptcode')

        if Company.objects.filter(symbol=symbol).exists():
            raise serializers.ValidationError("A company with this symbol already exists.")
        if Company.objects.filter(scriptcode=scriptcode).exists():
            raise serializers.ValidationError("A company with this scriptcode already exists.")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'symbol', 'scriptcode']


class WatchlistStockDetailSerializer(serializers.ModelSerializer):
    stock = CompanySerializer(source='stock_id', read_only=True)

    class Meta:
        model = WatchlistStockDetail
        fields = ('id', 'stock', 'created_on')


class WatchlistStockInputSerializer(serializers.Serializer):
    stock_id = serializers.IntegerField()


class WatchlistDetailSerializer(serializers.ModelSerializer):
    stocks = WatchlistStockInputSerializer(many=True, write_only=True)
    stock_details = WatchlistStockDetailSerializer(many=True, read_only=True, source='stocks')
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = WatchlistDetail
        fields = ['id', 'watchlist_name', 'stocks', 'stock_details', 'user_id', 'user_name']

    def create(self, validated_data):
        user = self.context['request'].user
        stocks_data = validated_data.pop('stocks')
        watchlist_name = validated_data.get('watchlist_name')

        # Check if watchlist already exists for the user
        watchlist, created = WatchlistDetail.objects.get_or_create(
            user=user,
            watchlist_name=watchlist_name,
            defaults={'watchlist_name': watchlist_name}
        )

        # Update stocks (clear and add new)
        for stock in stocks_data:
            company = get_object_or_404(Company, id=stock['stock_id'])
            WatchlistStockDetail.objects.create(watchlist=watchlist, stock_id=company)

        return watchlist


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class WatchlistListDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    stocks = WatchlistStockDetailSerializer(many=True)

    class Meta:
        model = WatchlistDetail
        fields = ['id', 'watchlist_name', 'user', 'stocks']


class RemoveWatchlistStockSerializer(serializers.Serializer):
    watchlist_id = serializers.IntegerField()
    stock_id = serializers.IntegerField()

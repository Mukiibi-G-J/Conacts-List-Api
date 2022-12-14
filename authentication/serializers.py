from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=8)
    first_name = serializers.CharField(max_length=255, min_length=2)
    first_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        # emaill= attrs.get("email", ')
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ["username", "password"]

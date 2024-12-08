from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    """
    Custom serializer extending Djoser's UserCreateSerializer
    Adds additional fields specific to our CustomUser model
    """
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'phoneNumber', 'email', 'fullName', 'cnic', 'user_type', 'password')
        extra_kwargs = {
            'phoneNumber': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True},
            'fullName': {'required': True},
            'cnic': {'required': True},
            'user_type': {'required': True}
        }
        
    def validate_user_type(self, value):
        """
        Check that users cannot register as ADMIN
        """
        if value == User.UserType.ADMIN:
            raise serializers.ValidationError("Cannot register as admin user.")
        return value
        
    def create(self, validated_data):
        """
        Override create method to properly handle user creation
        using our custom user manager
        """
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details
    """
    class Meta:
        model = User
        fields = ('id', 'phoneNumber', 'email', 'fullName', 'cnic', 'user_type', 'date_joined')
        read_only_fields = ('id', 'date_joined')
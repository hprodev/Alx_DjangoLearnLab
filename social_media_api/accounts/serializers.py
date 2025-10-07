from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creating new users with username, email, password.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
    
    def create(self, validated_data):
        """Create user and generate authentication token"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
        )
        # Create token for the new user
        Token.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile display.
    Shows user information without password.
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 
                  'followers_count', 'following_count']
    
    def get_followers_count(self, obj):
        """Count how many followers user has"""
        return obj.followers.count()
    
    def get_following_count(self, obj):
        """Count how many users this user follows"""
        return obj.following.count()
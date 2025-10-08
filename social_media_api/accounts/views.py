from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class RegisterView(generics.GenericAPIView):
    """
    View for user registration.
    Creates new user and returns authentication token.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    """
    View for user login.
    Returns authentication token for valid credentials.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View for viewing and updating user profile.
    Requires authentication.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the current logged-in user"""
        return self.request.user
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow another user and create notification.
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.add(user_to_follow)
        
        from notifications.models import Notification
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you'
        )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}'},
            status=status.HTTP_200_OK
        )
    
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    """
    try:
        user_to_unfollow = User.objects.get(id=user_id)
        
        # Remove from following list
        request.user.following.remove(user_to_unfollow)
        
        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}'},
            status=status.HTTP_200_OK
        )
    
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
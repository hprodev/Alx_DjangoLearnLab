from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Converts notification data to JSON.
    """
    actor_username = serializers.ReadOnlyField(source='actor.username')
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 
                'verb', 'timestamp', 'read']
        read_only_fields = ['recipient', 'actor', 'timestamp']

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user or request.user.is_anonymous:
            return False
        subcribe = request.user.follower.filter(author=obj)
        return subcribe.exists()

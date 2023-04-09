
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(UserSerializer):
    """Сериализтор пользователя."""
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
        """Проверка подписки."""
        request = self.context.get('request')
        user = request.user if request else None
        return (
            user and not user.is_anonymous
            and user.follower.filter(author=obj).exists()
        )

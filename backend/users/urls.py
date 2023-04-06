from django.contrib.auth import get_user_model
from django.urls import include, path

User = get_user_model()

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'))
]

from users.apps import UsersConfig
from django.urls import path

from users.views import UserCreateAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/update/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
]
from django.urls import path

from users.apps import UsersConfig
from users.views import UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListAPIView.as_view(), name="users-list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
]

from django.urls import path
from .views import UserListView, BlockUserView, DeleteUserView, UnblockUserView,BlockedUserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/block/', BlockUserView.as_view(), name='block-user'),
    path('users/delete/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
    path('users/<int:user_id>/unblock/', UnblockUserView.as_view(), name='unblock-user'),
    path('users/blocked/', BlockedUserListView.as_view(), name='blocked-user-list')
]

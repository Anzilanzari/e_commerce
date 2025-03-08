from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import UserSerializer


User = get_user_model()

# Custom permission: Only admin can access
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

#  View active users (Admins Only)
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admin can access

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_active=True)  # Exclude admins & blocked users


class BlockUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_staff:  # Prevent blocking other admins
                return Response({'error': 'Cannot block an admin'}, status=status.HTTP_403_FORBIDDEN)

            user.is_active = False  # Block user
            user.save()
            return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UnblockUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True  # Restore access
            user.save()
            return Response({'message': 'User unblocked successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class BlockedUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admin can access

    def get_queryset(self):
        return User.objects.filter(is_active=False)  # Show only blocked/soft-deleted users



User = get_user_model()

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can delete users

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_staff:  # Prevent deleting other admins
                return Response({'error': 'Cannot delete an admin'}, status=status.HTTP_403_FORBIDDEN)

            user.delete()  # Permanently delete the user from the database
            return Response({'message': 'User deleted permanently'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipesAPI.permissions import IsSelf
from recipesAPI.serializers import (CreateUserSerializer, GetUserSerializer,
                                    ProfileUserUpdateSerializer,
                                    SecurityUserUpdateSerializer)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'message': 'User created Successfully'},
            status=status.HTTP_201_CREATED
        )


class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    lookup_field = 'pk'


class ProfileUserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    lookup_field = 'pk'


class SecurityUserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SecurityUserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    lookup_field = 'pk'


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelf]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Send email confirmation
        return super().perform_destroy(instance)

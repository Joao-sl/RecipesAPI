from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipesAPI.serializers import UpdateUserSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        forbidden = ['GET', 'PATCH', 'DELETE']
        endswith_me = request.path.endswith('/me/') or \
            request.path.endswith('/me')
        endswith_me = request.path.rstrip('/').endswith('/me/')

        if request.method in forbidden and not endswith_me:
            raise MethodNotAllowed(
                method=request.method,
                detail='For GET, PATCH, DELETE use /api/user/me'
            )

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Send email confirmation
        return super().perform_destroy(instance)

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch', 'delete'],
        permission_classes=[IsAuthenticated],
        serializer_class=UpdateUserSerializer,
    )
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'DELETE':
            self.perform_destroy(user)

            return Response(status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from user.models import User
from ..serializers.user_serializers import UserSerializer, RegistrationSerializer, PasswordSerializer
from ..utils.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 是否為管理者
    permission_classes = [IsAdminUser]
    # 查詢參數(原預設pk)
    # lookup_field = 'username'

    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def reset_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save(request.user)
            data['response'] = 'successfully reset password.'
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(self.queryset, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
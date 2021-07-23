from rest_framework import viewsets
from django.contrib.auth.models import Group
from ..serializers.group_serializers import GroupSerializer
from rest_framework.permissions import IsAdminUser


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    # 全名
    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',  'last_name', 'first_name', 'full_name', 'groups', 'is_staff',
                  'is_active', 'is_superuser', 'last_login', 'date_joined')
        extra_kwargs = {
            # 只允許寫入
            'password': {'write_only': True},
            # 只允許讀取
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {
            # 只允許寫入
            'password': {'write_only': True},
            # 只允許讀取
        }

    def save(self):
        user = User(
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    def save(self, user):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        new_password2 = self.validated_data['new_password2']

        if not user.check_password(old_password):
            raise serializers.ValidationError({'password': 'Wrong password.'})
        elif new_password != new_password2:
            raise serializers.ValidationError({'password': 'New password must match.'})
        user.set_password(new_password)
        user.save()
        return user
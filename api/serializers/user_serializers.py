from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'groups', 'is_active', 'is_superuser', 'last_login', 'created_at', 'updated_at'
        )
        extra_kwargs = {
            # 只允許寫入
            'password': {'write_only': True},
            # 只允許讀取
            'last_login': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
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
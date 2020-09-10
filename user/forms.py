from django.forms import ModelForm
from django.contrib.auth.models import User


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name']

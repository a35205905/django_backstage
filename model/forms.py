from django.forms import ModelForm, CharField, PasswordInput, ModelMultipleChoiceField
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from model.services import get_content_types


class UserForm(ModelForm):
    password = CharField(
        label="密碼",
        strip=False,
        required=True,
        widget=PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'groups']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # 寫入多對多表
            self.save_m2m()
        return user


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'groups', 'is_active']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    group_users = ModelMultipleChoiceField(label='使用者', queryset=User.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        # 將使用者不需要的model排除
        content_types = get_content_types(settings.MODELS)
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__in=content_types)
        # 顯示群組裡的使用者
        if self.instance.id:
            user_ids = [user.id for user in self.instance.user_set.all()]
            self.fields['group_users'].initial = user_ids

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            # 寫入多對多表
            self.save_m2m()
        # 加入使用者
        group_users = group.user_set.all()
        group_set_users = self.cleaned_data["group_users"]
        group_remove_users = group_users.exclude(id__in=group_set_users)
        group_add_users = group_set_users.exclude(id__in=group_users)
        for user in group_remove_users:
            group.user_set.remove(user)
        for user in group_add_users:
            group.user_set.add(user)
        return group


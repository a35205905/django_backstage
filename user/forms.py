from django import forms
from django.contrib.auth import password_validation
from user.models import User


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': '新密碼不匹配',
    }
    new_password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': '請輸入新密碼'}),
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': '請再次輸新入密碼'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        print('clean_new_password2')
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "原密碼不正確",
        'password_repeat': '不能與原密碼相同',
    }
    old_password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': '請輸入原密碼', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password1(self):
        """
        Validate that the new_password2 field is repeat.
        """
        print('clean_new_password1')
        new_password1 = self.cleaned_data.get('new_password1')
        if self.user.check_password(new_password1):
            raise forms.ValidationError(
                self.error_messages['password_repeat'],
                code='password_repeat',
            )
        return new_password1

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserChangeForm, PasswordChangeForm


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/')

    return render(request, 'user/register.html', {'form': form})


@login_required
def password_change(request):
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    header = '密碼'
    if form.is_valid():
        form.save()
        logout(request)
        return redirect('/login/')

    return render(request, 'user/change.html', {'form': form, 'header': header})


@login_required
def user_change(request):
    form = UserChangeForm(data=request.POST or None, instance=request.user)
    header = '個人資訊'
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'user/change.html', {'form': form, 'header': header})


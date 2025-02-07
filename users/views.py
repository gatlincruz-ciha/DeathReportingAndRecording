from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('deathrr:home')
        else:
            form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': form})
    else:
        return redirect('deathrr:home')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')

@login_required(login_url="/users/login")
def reset_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Changed Successfully")
            return redirect('users:reset_password_success')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_reset.html', {'form': form})

def reset_password_successful_view(request):
    return render(request, 'users/password_reset_successful.html')
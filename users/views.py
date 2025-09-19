# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

@login_required
def user_list(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для просмотра этой страницы')
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_detail.html', {'user_profile': user})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
@login_required
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f'Пользователь {user.username} подтвержден!')
    return redirect('user_list')
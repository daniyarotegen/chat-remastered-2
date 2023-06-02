from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.shortcuts import redirect
from accounts.forms import ProfileForm

User = get_user_model()


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '')
        users = User.objects.exclude(id=request.user.id)
        if q:
            users = users.filter(Q(username__icontains=q))
        return render(request, 'profiles/user_list.html', {'users': users})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_user_model().objects.get(username=username)
        if request.user.username == username:
            return redirect('profile')
        return render(request, 'profiles/user_profile.html', {'user': user})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        return render(request, 'profiles/profile.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'profiles/edit_profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
        return render(request, 'profiles/edit_profile.html', {'form': form})

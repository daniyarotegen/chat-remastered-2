from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        return render(request, 'profiles/profile.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'profiles/edit_profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
        return render(request, 'profiles/edit_profile.html', {'form': form})



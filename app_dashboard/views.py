from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from app_account.models import User
from .forms import UserInfoForm, ChangePasswordForm


# Create your views here.


class Dashboard(View):
    template_name = "app_dashboard/dashboard.html"

    def get(self, request, pk):
        user_page = get_object_or_404(User, id=pk)
        context = {
            'user_page': user_page,
        }
        return render(request, 'app_dashboard/dashboard.html', context)


class ChangeUserInfoView(View):
    def get(self,request):
        current_user= User.objects.filter(id=request.user.id).first()
        form = UserInfoForm(instance=current_user)
        context={
            'current_user': current_user,
            'form':form,
        }
        return render(request, 'app_dashboard/user_change_information.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = UserInfoForm(instance=current_user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been successfully saved.', 'secondary')
        context={
            'current_user': current_user,
            'form':form,
        }
        return render(request, 'app_dashboard/user_change_information.html', context)


class ChangePasswordView(View):
    def get(self, request):
        user_page = User.objects.filter(id=request.user.id).first()
        form = ChangePasswordForm()
        context = {
            'user_page': user_page,
            'form': form
        }
        return render(request, 'app_dashboard/user_change_password.html', context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user_page = User.objects.filter(id=request.user.id).first()
            if user_page.check_password(form.cleaned_data.get('current_password')):
                user_page.set_password(form.cleaned_data.get('new_password'))
                user_page.save()
                logout(request)
                messages.success(request, 'Your password is changed successfully, please login with your new password',
                                 'secondary')
                return redirect('app_account:login_page')
            else:
                form.add_error('current_password', 'Your password is wrong!')

        context = {
            'user_page': user_page,
            'form': form,
        }
        return render(request, 'app_dashboard/user_change_password.html', context)







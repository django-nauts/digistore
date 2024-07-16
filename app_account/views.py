import json

from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View

from utils.email_service import send_email_to_user
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from .models import User
from app_cart.cart import Cart


# Create your views here.

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'app_account/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email').lower()
            password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'Your account is not activated yet.')
                else:
                    is_password_correct = user.check_password(password)
                    if is_password_correct:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                        # Update user basket after login
                        current_user = User.objects.get(id=request.user.id)
                        user_id = current_user.id
                        saved_cart = current_user.user_cart
                        print(saved_cart)
                        if saved_cart:
                            converted_cart = json.loads(saved_cart)
                            cart = Cart(request)
                            # loop thru the cart
                            # example of cart: {"1": {"price": "10.54", "qty": 4}, "2": {"price": "5.68", "qty": 5}}
                            for key, value in converted_cart.items():
                                qty = value['qty']
                                price = value['price']
                                cart.db_add(product_id=key, qty=qty, price=price)

                        messages.success(request, 'You login successfully.', 'secondary')
                        return redirect('app_home:home_page')
                    else:
                        login_form.add_error('Your email or password is wrong.')
            else:
                login_form.add_error('email', 'Your not registered, please sign up first!')
        context = {
            'login_form': login_form,
        }
        return render(request, 'app_account/login.html', context)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'app_account/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email').lower()
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'You already registered with that email.')
            else:
                new_user = User(
                    email=user_email,
                    username=username,
                    is_active=False,
                    email_active_code=get_random_string(72),
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email_to_user('Activation code in Digistore', new_user.email, {'user': new_user},
                                   'emails/activation_email.html')
                messages.success(request, 'You registered successfully', 'secondary')
                return redirect('app_home:home_page')
        context = {
            'register_form': register_form
        }
        return render(request, 'app_account/register.html', context)


class ForgetPasswordView(View):
    def get(self, request):
        forget_pass_form = ForgetPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'app_account/forget_pass.html', context)

    def post(self, request):
        forget_pass_form = ForgetPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email').lower()
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email_to_user('Reset your password on Digistore', user.email, {'user': user},
                                   'emails/forget_password_email.html')
                messages.success(request, 'Your password os changed successfully.', 'secondary')
                return redirect('app_home:home_page')

        context = {
            'forget_pass_form': forget_pass_form,
        }
        return render(request, 'app_account/forget_pass.html', context)


class ResetPasswordView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is None:
            messages.error(request, 'Your activation code does not exist.', extra_tags='warning'),
            return redirect('app_home:home_page')
        else:
            reset_password_form = ResetPasswordForm()
            context = {
                'reset_password_form': reset_password_form,
                'user': user,
            }
            return render()

    def post(self, request, email_active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if reset_password_form.is_valid():
            if user is None:
                return redirect('app_account:login_page')
            new_password = reset_password_form.cleaned_data.get('password')
            user.set_password(new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()

        context = {
            'reset_password_form': reset_password_form,
            'user': user,
        }
        return render(request, 'app_account/reset_pass.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'Your account is activated successfully, you can login now.', 'secondary')
                return redirect('app_account:login_page')
            else:
                pass
        raise Http404


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('app_account:login_page')

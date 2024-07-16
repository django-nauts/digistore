from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.template.loader import render_to_string

from app_account.models import User
from app_payment.models import ShippingAddress
from .forms import UserInfoForm, ChangePasswordForm


# Create your views here.


class Dashboard(View):
    template_name = "app_dashboard/dashboard.html"

    def get(self, request):
        user_page = get_object_or_404(User, id=request.user.id)
        context = {
            'user_page': user_page,
        }
        return render(request, 'app_dashboard/dashboard.html', context)


class ChangeUserInfoView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = UserInfoForm(instance=current_user)
        context = {
            'current_user': current_user,
            'form': form,
        }
        return render(request, 'app_dashboard/user_change_information.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = UserInfoForm(instance=current_user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been successfully saved.', 'secondary')
        context = {
            'current_user': current_user,
            'form': form,
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


class ShippingAddressView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        shipping_addresses = ShippingAddress.objects.filter(user__id=request.user.id)
        context = {
            'shipping_addresses': shipping_addresses,
            'current_user': current_user,
        }
        return render(request, 'app_dashboard/change_address.html', context)


def shipping_address_delete(request):
    if request.method == 'POST':
        ship_id = request.POST.get('shipId')
        shipping_address = ShippingAddress.objects.filter(id=ship_id).delete()
        context = {
            'success': True,
        }
        return JsonResponse(context)


def chosen_shipping_address(request):
    if request.method == 'POST':
        user_id = request.user.id
        full_name = request.POST.get('fullname')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        email = request.POST.get('email')
        shipping_address = ShippingAddress(user_id=user_id, full_name=full_name, city=city, state=state,
                                           zipcode=zipcode, address=address, email=email, main_address=True)
        shipping_address.save()
        other_shipping_addresses = ShippingAddress.objects.filter(main_address=True).exclude(id=shipping_address.id)
        if other_shipping_addresses:
            for shipping_add in other_shipping_addresses:
                shipping_add.main_address = False
                shipping_add.save()
        shipping_addresses = ShippingAddress.objects.filter(user_id=user_id)

        context = {
            'shipping_addresses': shipping_addresses
        }
        return render(request, 'app_dashboard/change_address_area.html', context)
    return HttpResponse('Ajaxify by Ventuno')


def check_shipping_address(request):
    if request.method == 'POST':
        check_status = request.POST.get('check_status')
        ship_add_id = request.POST.get('shipAddId')
        shipping_address = ShippingAddress.objects.get(id=ship_add_id)

        print("++++++++++++++++++++++++++++++++++++++++++++++++")
        print(check_status)
        print(shipping_address)
        print("++++++++++++++++++++++++++++++++++++++++++++++++")

        if check_status == "true":
            shipping_address.main_address = False
            shipping_address.save()

            shipping_addresses = ShippingAddress.objects.filter(user_id=request.user.id)
            context = {
                'shipping_addresses': shipping_addresses,
            }
            return JsonResponse({'body': render_to_string('app_dashboard/change_address_area.html', context),
                                 'check_status': 'unchecked'})

        else:
            shipping_address.main_address = True
            shipping_address.save()

            other_shipping_addresses = ShippingAddress.objects.filter(main_address=True).exclude(id=shipping_address.id)

            if other_shipping_addresses:
                for shipping_add in other_shipping_addresses:
                    shipping_add.main_address = False
                    shipping_add.save()
            shipping_addresses = ShippingAddress.objects.filter(user_id=request.user.id)
            context = {
                'shipping_addresses': shipping_addresses,
            }
            body = render_to_string('app_dashboard/change_address_area.html', context)
            return JsonResponse({'body': body, 'check_status': 'checked'})

        return HttpResponse('Ajaxify by Ventuno')

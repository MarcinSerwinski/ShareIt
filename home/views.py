from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.contrib.auth.models import User
from pytest_django.fixtures import django_user_model
from django.contrib import messages
from home import forms
from home.models import *


class LandingPage(View):

    def get(self, request):
        sum_of_bags = Donation.objects.aggregate(Sum('quantity'))
        sum_of_institutions = Institution.objects.count()
        fundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_charities = Institution.objects.filter(type=3)

        return render(request, 'home/index.html',
                      {'sum_of_bags': sum_of_bags, 'sum_of_institutions': sum_of_institutions,
                       'fundations': fundations, 'organizations': organizations, 'local_charities': local_charities})


class AddDonation(LoginRequiredMixin, View):
    login_url = 'home:login'
    template_name = 'home/form.html'
    model = Donation

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, self.template_name, {'categories': categories, 'institutions': institutions})

    def post(self, request):
        quantity = request.POST.get('quantity')
        categories = request.POST.get('category')
        institution = request.POST.get('organization')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        user = request.user

        donation = Donation(quantity=quantity, institution_id=institution, address=address,
                            phone_number=phone_number, city=city, zip_code=zip_code, pick_up_date=pick_up_date,
                            pick_up_time=pick_up_time, user=user)
        donation.save()
        donation.categories.add(categories)
        return redirect('home:home')


class Register(View):
    template_name = 'home/register.html'
    model = get_user_model()

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User()
            user.username = email
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            return redirect('home:login')
        else:
            return render(request, self.template_name, {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')

        else:
            return redirect('home:register')
    else:
        return render(request, 'home/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('home:home')


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        users = get_user_model()
        user = users.objects.get(pk=request.user.pk)
        donations = Donation.objects.filter(user=user.pk)

        return render(request, 'home/user.html', {'user': user, 'donations': donations})

    def post(self, request):
        users = get_user_model()
        user = users.objects.get(pk=request.user.pk)
        donations = Donation.objects.filter(user=user)
        id_donation = request.POST.get('id_donation')
        donation = donations.get(pk=id_donation)

        if donation.is_taken:

            donation.is_taken = False
            donation.save()

        elif not donation.is_taken:

            donation.is_taken = True
            donation.save()

        return redirect('home:profile')


class AccessEditUser(LoginRequiredMixin, View):
    template_name = 'home/edit-user-access.html'

    def get(self, request):
        form = forms.UserEditAccessForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UserEditAccessForm(request.POST)
        if form.is_valid():
            password_entered = form.cleaned_data['password']
            user_password = request.user.password
            authenticate_user = check_password(password_entered, user_password)
            if authenticate_user:
                return redirect('home:home')

            else:
                messages.error(request, ("Podano nieprawidłowe hasło."))
                return redirect('home:access-edit-user')

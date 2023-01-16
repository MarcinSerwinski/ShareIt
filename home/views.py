import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.contrib.auth.models import User

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
        categories = request.POST['categories']


class Register(View):
    template_name = 'home/register.html'
    model = User

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

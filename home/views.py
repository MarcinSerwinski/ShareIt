from django.shortcuts import render
from django.views.generic import TemplateView, FormView


class LandingPage(TemplateView):
    template_name = 'home/index.html'

class AddDonation(TemplateView):
    template_name = 'home/form.html'

class Login(TemplateView):
    template_name = 'home/login.html'

class Register(TemplateView):
    template_name = 'home/register.html'
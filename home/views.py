from django.shortcuts import render
from django.views.generic import TemplateView, FormView


class LandingPage(TemplateView):
    template_name = 'home/index.html'

class AddDonation(TemplateView):
    template_name = 'home/form.html'
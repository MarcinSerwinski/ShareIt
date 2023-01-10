from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from home.models import Donation, Institution


class LandingPage(View):

    def get(self, request):
        sum_of_bags = Donation.objects.aggregate(Sum('quantity'))
        sum_of_institutions = Institution.objects.count()
        return render(request, 'home/index.html',
                      {'sum_of_bags': sum_of_bags, 'sum_of_institutions': sum_of_institutions})


class AddDonation(TemplateView):
    template_name = 'home/form.html'


class Login(TemplateView):
    template_name = 'home/login.html'


class Register(TemplateView):
    template_name = 'home/register.html'

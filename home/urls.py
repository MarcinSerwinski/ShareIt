from django.urls import path

from . import views
from home.views import *

app_name = 'home'

urlpatterns = [
    path('', LandingPage.as_view(), name='home'),
    path('add-donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
]

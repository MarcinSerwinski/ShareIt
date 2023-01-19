from django.urls import path

from . import views
from home.views import *

app_name = 'home'

urlpatterns = [
    path('', LandingPage.as_view(), name='home'),
    path('add-donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', views.login_view, name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', Profile.as_view(), name='profile'),
]

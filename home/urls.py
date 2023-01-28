from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
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
    path('user/edit/', AccessEditUser.as_view(), name='access-edit-user'),
    path('user/edit/details', EditUser.as_view(), name='edit-user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('contact/', Contacts.as_view(), name='contact'),
    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.activate_new_password, name='password_reset_confirms'),
]

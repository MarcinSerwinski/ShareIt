from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from home import forms
from home.models import *
from .tokens import account_activation_token


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('home:login')
        else:
            return render(request, self.template_name, {'form': form})


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('home/template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Drogi {user}, przejdź do swojej skrzynki pocztowej w celu aktywacji konta.')
    else:
        messages.error(request,
                       f'Pojawił się problem z wysłaniem maila na {to_email}, sprawdź czy nie popełniłeś literówki.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Dziękujemy za potwierdzenie emaila. Możesz się teraz zalogować.')
        return redirect('home:login')
    else:
        messages.error(request, 'Link do aktywacji nie działa!')

    return redirect('home:home')


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
    template_name = 'home/user.html'

    def get(self, request):
        users = get_user_model()
        user = users.objects.get(pk=request.user.pk)
        donations = Donation.objects.filter(user=user.pk)

        return render(request, self.template_name, {'user': user, 'donations': donations})

    def post(self, request):
        users = get_user_model()
        user = users.objects.get(pk=request.user.pk)
        donations = Donation.objects.filter(user=user).order_by('pick_up_date')
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
                return redirect('home:edit-user')

            else:
                messages.error(request, "Podano nieprawidłowe hasło.")
                return redirect('home:access-edit-user')


class EditUser(LoginRequiredMixin, View):
    template_name = 'home/edit-user.html'

    def get(self, request):
        form = forms.UserEditForm()
        form_password = forms.UserEditPasswordForm()

        return render(request, self.template_name, {'form': form, 'form_password': form_password})

    def post(self, request):
        users = get_user_model()
        user = users.objects.get(pk=request.user.pk)
        form = forms.UserEditForm(request.POST)
        form_password = forms.UserEditPasswordForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['email']
            user.save()
            messages.success(request, "Zmieniono dane.")
            return redirect('home:edit-user')

        if form_password.is_valid():
            old_password = form_password.cleaned_data['old_password']
            password1 = form_password.cleaned_data['password1']
            password2 = form_password.cleaned_data['password2']
            if user.check_password(old_password):
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    return redirect('home:profile')
                else:
                    messages.error(request, 'Podane hasła nie są takie same!')
                    return redirect('home:edit-user')
            else:
                messages.error(request, 'Stare hasło jest niepoprawne!')
                return redirect('home:edit-user')

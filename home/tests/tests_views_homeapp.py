from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.messages import get_messages
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertTemplateUsed
from home.forms import UserEditPasswordForm, UserEditForm, RegistrationForm, UserEditAccessForm, NewPasswordForm, \
    UserLoginForm
from home.models import *
from home.tokens import account_activation_token


def test_landing_page_get(db, client):
    endpoint = reverse('home:home')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h2>Wystarczą 4 proste kroki</h2>' in response.content.decode('UTF-8')
    assert '<h3>Zdecyduj komu chcesz pomóc</h3>' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'home/index.html')
    assertTemplateUsed(response, 'base.html')
    assertTemplateUsed(response, 'partials/_menu.html')


def test_registration_page_get(client):
    endpoint = reverse('home:register')
    response = client.get(endpoint)
    form_in_url = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_url, RegistrationForm)
    assertTemplateUsed(response, 'home/register.html')


def test_registration_page_post(db, client, user):
    form_url = reverse('home:register')
    data = {'first_name': 'TestFirstName', 'last_name': 'TestLastName', 'email': 'test@email.com',
            'password1': 'PasswordNotTooShortNotTooWeak1!', 'password2': 'PasswordNotTooShortNotTooWeak1!'}
    response = client.post(form_url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('home:login'))
    assert User.objects.get(is_active=False)


def test_login_page_get(client, user):
    endpoint = reverse('home:login')
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, UserLoginForm)
    assertTemplateUsed(response, 'home/login.html')


def test_login_page_post(client, user):
    form_url = reverse('home:login')
    data = {'username': 'test2@admin.com', 'password': 'TestPass123!'}
    response = client.post(form_url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    assert auth.get_user(client).is_authenticated


def test_add_donation_get(client, user):
    client.force_login(user)
    endpoint = reverse('home:add-donation')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h3>Zaznacz co chcesz oddać:</h3>' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'home/form.html')


def test_add_user_not_logged_donation_get(client, user):
    endpoint = reverse('home:add-donation')
    response = client.get(endpoint)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:login'))


def test_add_donation_post(db, client, user, create_institution, create_category):
    client.force_login(user)
    form_url = reverse('home:add-donation')

    data = {'quantity': 1, 'address': 'testAddress', 'category': create_category.pk,
            'organization': create_institution.pk, 'phone': '123123123', 'city': 'testCity',
            'postcode': '12-123',
            'data': '2023-01-23', 'time': '12:30', 'user': user}

    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    assert Donation.objects.get(address='testAddress')


def test_user_donations_details_get(db, client, user, create_donation):
    client.force_login(user)
    endpoint = reverse('home:profile')
    response = client.get(endpoint)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home/user.html')
    assert "test2@admin.com" in response.content.decode('UTF-8')
    assert "TestAddress" in response.content.decode('UTF-8')
    assert Donation.objects.get(is_taken=False)


def test_user_donations_details_post(db, client, user, create_donation):
    client.force_login(user)
    endpoint = reverse('home:profile')

    # Check if toggling is_taken value from False to True works:
    data = {'id_donation': create_donation.pk}
    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:profile'))
    assert Donation.objects.get(is_taken=True)

    # Check if toggling is_taken value from True to False works:
    data = {'id_donation': create_donation.pk}
    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:profile'))
    assert Donation.objects.get(is_taken=False)


def test_user_access_to_edit_get(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:access-edit-user')
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, UserEditAccessForm)


def test_user_access_to_edit_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:access-edit-user')
    data = {'password': 'TestPass123!'}

    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:edit-user'))


def test_user_no_access_to_edit_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:access-edit-user')
    data = {'password': 'ThisIsWrongPassword'}

    response = client.post(endpoint, data)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:access-edit-user'))
    assert str(messages[0]) == "Podano nieprawidłowe hasło."


def test_user_edit_get(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:edit-user')
    response = client.get(endpoint)
    form_in_view = response.context['form']
    form2_in_view = response.context['form_password']

    assert response.status_code == 200
    assertTemplateUsed(response, 'home/edit-user.html')
    assert isinstance(form_in_view, UserEditForm)
    assert isinstance(form2_in_view, UserEditPasswordForm)


def test_user_edit_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:edit-user')
    data = {'first_name': 'Name', 'last_name': 'Surname', 'email': 'test@a.com'}

    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:edit-user'))


def test_user_edit_password_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:edit-user')
    data = {'old_password': 'TestPass123!', 'password1': 'NewTestPass123', 'password2': 'NewTestPass123'}
    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:profile'))
    assert user.check_password(data.get('old_password'))


def test_user_edit_passwords_are_not_the_same_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:edit-user')
    data = {'old_password': 'TestPass123!', 'password1': 'NewPass123', 'password2': 'NewTestPass123'}
    response = client.post(endpoint, data)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:edit-user'))
    assert user.check_password(data.get('old_password'))
    assert str(messages[0]) == "Podane hasła nie są takie same!"


def test_user_edit_old_password_is_incorrect_post(db, client, user):
    client.force_login(user)
    endpoint = reverse('home:edit-user')
    data = {'old_password': 'OldPassWrong111', 'password1': 'NewTestPass123', 'password2': 'NewTestPass123'}
    response = client.post(endpoint, data)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:edit-user'))
    assert not user.check_password(data.get('old_password'))
    assert str(messages[0]) == "Stare hasło jest niepoprawne!"


def test_contact_email_send(db, client):
    endpoint = reverse('home:contact')
    data = {'name': 'ContactName', 'surname': 'ContactSurname', 'message': 'ContactMessage'}
    response = client.post(endpoint, data)
    # Create email test case:
    mail_subject = 'Zapytanie od użytkownika strony'
    message = f"Imię: {data['name']}, Nazwisko: {data['surname']}. Zapytanie: {data['message']}"
    mail.send_mail(mail_subject, message, 'from@djangoapp.com', ['to@someone.com'])

    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    # Testing email:
    assert len(mail.outbox) == 2
    assert mail.outbox[0].body == "Imię: ContactName, Nazwisko: ContactSurname. Zapytanie: ContactMessage"
    assert mail.outbox[0].subject == 'Zapytanie od użytkownika strony'


def test_password_reset_view_get(client):
    endpoint = reverse('home:password_reset')
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, PasswordResetForm)
    assertTemplateUsed(response, 'home/password_reset_form.html')


def test_password_reset_view_post(db, client, user):
    endpoint = reverse('home:password_reset')
    data = {'email': 'test2@admin.com'}
    response = client.post(endpoint, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('home:password_reset_done'))
    # Testing reset password email:
    domain = response.context['domain']
    protocol = response.context['protocol']
    token = response.context['token']
    uid = response.context['uid']
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Przypomnienie hasła"
    assert mail.outbox[
               0].body == f'\nCześć,\n\nKliknij w poniższy link aby resetować hasło:\n\n\n{protocol}://{domain}/reset' \
                          f'-password/confirm/{uid}/{token}/\n\n'


def test_password_reset_view_wrong_email_post(db, client):
    endpoint = reverse('home:password_reset')
    data = {'email': 'user_does_not_exist@email.com'}
    response = client.post(endpoint, data)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:password_reset'))
    assert str(messages[0]) == 'Użytkownik o podanym emailu nie istnieje!'
    # Testing if no email has been sent:
    assert len(mail.outbox) == 0


def test_activate_new_password_correct_token_uidb64_get(client, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    endpoint = reverse('home:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, NewPasswordForm)


def test_activate_new_password_wrong_token_uidb64_get(client, user):
    uid = 'wrong'
    token = 'wrong'
    endpoint = reverse('home:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    response = client.get(endpoint)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    assert str(messages[0]) == "Link nie działa - wygeneruj zapytanie jeszcze raz."


def test_activate_new_password_post(client, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    endpoint = reverse('home:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    data = {'new_password1': 'VeryStrongNewPassword1!', 'new_password2': 'VeryStrongNewPassword1!'}
    response = client.post(endpoint, data)
    user_with_updated_password = User.objects.get(username="test2@admin.com")
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    # Check if password has been changed:
    assert user_with_updated_password.check_password(data.get('new_password1'))


def test_activate_new_account_get(client, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    endpoint = reverse('home:activate', kwargs={'uidb64': uid, 'token': token})
    response = client.get(endpoint)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:login'))
    assert str(messages[0]) == 'Dziękujemy za potwierdzenie emaila. Możesz się teraz zalogować.'


def test_activate_new_account_wrong_token_uidb64_gt(client, user):
    uid = 'wrong'
    token = 'wrong'
    endpoint = reverse('home:activate', kwargs={'uidb64': uid, 'token': token})
    response = client.get(endpoint)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:home'))
    assert str(messages[0]) == 'Link do aktywacji nie działa!'

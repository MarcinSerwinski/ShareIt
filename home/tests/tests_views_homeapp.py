from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from home.models import *


def test_landing_page_get(db,client):
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
    assert response.status_code == 200
    assertTemplateUsed(response, 'home/register.html')


def test_registration_page_post(db, client):
    form_url = reverse('home:register')
    data = {'first_name': 'TestFirstName', 'last_name': 'TestLastName', 'email': 'test@email.com',
            'password1': 'testpass', 'password2': 'testpass'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:login'))
    assert User.objects.get(first_name='TestFirstName')


def test_login_page_get(client, user):
    client.force_login(user)
    endpoint = reverse('home:login')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '>Ustawienia</a></li>' in str(response.content)
    assertTemplateUsed(response, 'home/login.html')


def test_add_donation_get(client, user):
    client.force_login(user)
    endpoint = reverse('home:add-donation')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h3>Zaznacz co chcesz oddać:</h3>' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'home/form.html')


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
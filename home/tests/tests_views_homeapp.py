from django.urls import reverse

from home.models import *


def test_landing_page_get(db, client):
    endpoint = reverse('home:home')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h2>Wystarczą 4 proste kroki</h2>' in response.content.decode('UTF-8')
    assert '<h3>Zdecyduj komu chcesz pomóc</h3>' in response.content.decode('UTF-8')


def test_registration_page_get(db, client):
    endpoint = reverse('home:register')
    response = client.get(endpoint)
    assert response.status_code == 200


def test_registration_page_post(db, client):
    form_url = reverse('home:register')
    data = {'first_name': 'TestFirstName', 'last_name': 'TestLastName', 'email': 'test@email.com',
            'password1': 'testpass', 'password2': 'testpass'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home:login'))
    assert User.objects.get(first_name='TestFirstName')
from django.urls import reverse

from home.models import *

def test_landing_page_get(db, client):
    endpoint = reverse('home:home')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h2>Wystarczą 4 proste kroki</h2>' in response.content.decode('UTF-8')
    assert '<h3>Zdecyduj komu chcesz pomóc</h3>' in response.content.decode('UTF-8')

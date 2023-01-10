import pytest

from home.models import *

@pytest.fixture()
def create_category(db):
    return Category.objects.create(name='TestNameCategory')


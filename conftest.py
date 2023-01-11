import pytest

from home.models import *

@pytest.fixture()
def create_category(db):
    return Category.objects.create(name='TestNameCategory')

@pytest.fixture()
def create_institution(db, create_category):
    institution_types = [(1, 'Fundacja'),
                         (2, 'Organizacja pozarządowa'),
                         (3, 'Zbiórka lokalna')]
    return Institution.objects.create(name='TestNameInstitution',
                                      description='TestDescriptionInstitution',
                                      type=institution_types[0][0],
                                      )
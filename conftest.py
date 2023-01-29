import pytest


from home.models import *


@pytest.fixture()
def user(db, django_user_model):
    """Create django user"""
    return django_user_model.objects.create_user(username='test2@admin.com', email='test2@admin.com',
                                                 password='TestPass123')


@pytest.fixture()
def create_category(db):
    """Create model Category"""
    return Category.objects.create(name='TestNameCategory')


@pytest.fixture()
def create_institution(db, create_category):
    """Create model Institution"""
    institution_types = [(1, 'Fundacja'),
                         (2, 'Organizacja pozarządowa'),
                         (3, 'Zbiórka lokalna')]

    institution = Institution.objects.create(name='TestNameInstitution',
                                             description='TestDescriptionInstitution',
                                             type=institution_types[0][0])
    institution.categories.set([create_category])
    return institution


@pytest.fixture()
def create_donation(db, create_category, create_institution, user):
    """Create model Donation"""
    donation = Donation.objects.create(quantity=1,
                                       address='TestAddress',
                                       phone_number='1234567890',
                                       institution_id=create_institution.pk,
                                       city='TestCity',
                                       zip_code='123-123',
                                       pick_up_date='2023-01-23',
                                       pick_up_time='12:30',
                                       user_id=user.id,
                                       is_taken=False)
    donation.categories.set([create_category])
    return donation



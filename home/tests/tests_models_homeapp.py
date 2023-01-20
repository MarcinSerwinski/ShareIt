from home.models import *


def test_create_user(user, django_user_model):
    users = django_user_model.objects.all()
    assert len(users) == 1


def test_category_content(create_category):
    category = Category.objects.all()
    assert create_category.name == 'TestNameCategory'
    assert len(category) == 1


def test_institution_content(create_institution):
    institution = Institution.objects.all()
    assert create_institution.categories.filter(name='TestNameCategory')
    assert create_institution.name == 'TestNameInstitution'
    assert create_institution.description == 'TestDescriptionInstitution'
    assert create_institution.type == 1
    assert len(institution) == 1



def test_donation_content(create_donation):
    donation = Donation.objects.all()
    assert create_donation.institution.name == 'TestNameInstitution'
    assert create_donation.categories.filter(name='TestNameCategory')
    assert create_donation.quantity == 1
    assert create_donation.address == 'TestAddress'
    assert create_donation.phone_number == '1234567890'
    assert create_donation.city == 'TestCity'
    assert create_donation.zip_code == '123-123'
    assert create_donation.pick_up_date == '2023-01-23'
    assert create_donation.pick_up_time == '12:30'
    assert len(donation) == 1

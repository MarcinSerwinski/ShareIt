from home.models import *


def test_category_content(create_category):
        category = Category.objects.all()
        assert create_category.name == 'TestNameCategory'
        assert len(category) == 1

def test_institution_content(create_institution):
        institution = Institution.objects.all()
        assert create_institution.name == 'TestNameInstitution'
        assert create_institution.description == 'TestDescriptionInstitution'
        assert create_institution.type == 1
        assert len(institution) == 1
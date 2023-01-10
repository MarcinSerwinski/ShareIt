from home.models import Category


def test_category_content(create_category):
        assert create_category.name == 'TestNameCategory'
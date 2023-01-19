from pytest_factoryboy import register

from tests.factories import VacancyFactory


# Fixtures
pytest_plugins = "tests.fixtures"


# Factories
register(VacancyFactory)

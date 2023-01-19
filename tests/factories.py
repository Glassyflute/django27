import factory

from vacancies.models import Vacancy


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    slug = "test"
    text = "test text"


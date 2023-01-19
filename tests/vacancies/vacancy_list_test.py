from datetime import datetime

import pytest

from tests.factories import VacancyFactory
from vacancies.models import Vacancy
from vacancies.serializers import VacancyListSerializer


@pytest.mark.django_db
def test_list_view(client):
    vacancies = VacancyFactory.create_batch(5)

    response = client.get("/vacancy/")

    expected_response = {
        'count': 5,
        'next': None,
        'previous': None,
        'results': VacancyListSerializer(vacancies, many=True).data
    }

    assert response.status_code == 200
    assert response.data == expected_response


# @pytest.mark.django_db
# def test_list_view(client):
#     vacancy = Vacancy.objects.create(
#         slug="test",
#         text="test text"
#     )
#
#     expected_response = {
#         'count': 1,
#         'next': None,
#         'previous': None,
#         'results': [{
#             "id": vacancy.pk,
#             "slug": "test",
#             "text": "test text",
#             "status": "draft",
#             "created": datetime.now().strftime("%Y-%m-%d"),
#             "username": None,
#             "skills": []
#         }]
#     }
#
#     response = client.get("/vacancy/")
#
#     assert response.status_code == 200
#     assert response.data == expected_response


from datetime import datetime

import pytest

from vacancies.models import Vacancy


@pytest.mark.django_db
def test_vacancy_detail(client, vacancy, hr_token):
    expected_response = {
        "id": vacancy.pk,
        "slug": "test",
        "text": "test text",
        "status": "draft",
        "created": datetime.now().strftime("%Y-%m-%d"),
        # "min_experience": None,
        "skills": [],
        "user": None
    }

    response = client.get(f"/vacancy/{vacancy.pk}/",
                          content_type="application/json",
                          HTTP_AUTHORIZATION="Token " + hr_token)

    assert response.status_code == 200
    assert response.data == expected_response

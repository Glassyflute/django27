import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from django27 import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyDetailSerializer, VacancyListSerializer, VacancyCreateSerializer


def hello(request):
    return HttpResponse("Hello world")


# @csrf_exempt for functions before without CBV
# @method_decorator(csrf_exempt, name="dispatch") for CBV but not here
class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        self.object_list = self.object_list.order_by("slug")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # vacancies = []
        # for vacancy in page_obj:
        #     vacancies.append(
        #         {
        #             "id": vacancy.id,
        #             "text": vacancy.text,
        #             "slug": vacancy.slug,
        #             "status": vacancy.status,
        #             "created": vacancy.created,
        #             "user": vacancy.user_id,
        #             "skills": list(map(str, vacancy.skills.all()))
        #         }
        #     )
        list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_obj))

        response = {
            "items": VacancyListSerializer(page_obj, many=True).data,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        # return JsonResponse({
        #     "id": vacancy.id,
        #     "text": vacancy.text,
        #     "slug": vacancy.slug,
        #     "status": vacancy.status,
        #     "created": vacancy.created,
        #     "user": vacancy.user_id,
        #     "skills": list(map(str, vacancy.skills.all()))
        # })
        return JsonResponse(VacancyDetailSerializer(vacancy).data)


@method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
        if vacancy_data.is_valid():
            vacancy_data.save()
        else:
            return JsonResponse(vacancy_data.errors)

        return JsonResponse(vacancy_data.data)

        # vacancy_data = json.loads(request.body)
        #
        # vacancy = Vacancy.objects.create(
        #     slug=vacancy_data["slug"],
        #     text=vacancy_data["text"],
        #     status=vacancy_data["status"]
        # )

        # vacancy.user = User.objects.get(pk=vacancy_data["user_id"])
        # vacancy.user = get_object_or_404(User, pk=vacancy_data["user_id"])
        #
        # for skill in vacancy_data["skills"]:
        #     skill_obj, created = Skill.objects.get_or_create(
        #         name=skill,
        #         defaults={
        #             "is_active": True
        #         }
        #     )
        #     vacancy.skills.add(skill_obj)
        #
        # vacancy.save()

        # return JsonResponse({
        #             "id": vacancy.id,
        #             "text": vacancy.text,
        #             "slug": vacancy.slug,
        #             "status": vacancy.status,
        #             "created": vacancy.created,
        #             "user": vacancy.user_id,
        #             "skills": list(map(str, vacancy.skills.all()))
        #         })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["slug", "text", "status", "skills"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)
        self.object.slug = vacancy_data["slug"]
        self.object.text = vacancy_data["text"]
        self.object.status = vacancy_data["status"]

        for skill in vacancy_data["skills"]:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"error": "skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
                    "id": self.object.id,
                    "text": self.object.text,
                    "slug": self.object.slug,
                    "status": self.object.status,
                    "created": self.object.created,
                    "user": self.object.user_id,
                    "skills": list(map(str, self.object.skills.all()))
                })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "name": user.username,
                    "vacancies": user.vacancies
                }
            )

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "average_num_vacancies": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
        }

        return JsonResponse(response)


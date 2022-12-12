from django.db import models


class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта")
    ]

    text = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=50)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateField()

    def __str__(self):
        return self.slug


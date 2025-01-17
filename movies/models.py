from django.db import models

from chats.models import QueryableModel


class Movie(QueryableModel):
    class Status(models.TextChoices):
        RUMORED = "Rumored"
        PLANNED = "Planned"
        IN_PRODUCTION = "In Production"
        POST_PRODUCTION = "Post Production"
        RELEASED = "Released"
        CANCELED = "Canceled"

    title = models.CharField(max_length=255)
    genres = models.ManyToManyField("Genre", blank=True)
    original_language = models.ForeignKey("Language", on_delete=models.CASCADE)
    overview = models.TextField(null=True)
    popularity = models.FloatField()
    production_companies = models.ManyToManyField("Company", blank=True)
    release_date = models.DateField(null=True)
    budget = models.PositiveBigIntegerField()
    revenue = models.PositiveBigIntegerField()
    runtime = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    tagline = models.TextField(null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    credits = models.ManyToManyField("Contributor", blank=True)
    keywords = models.ManyToManyField("Keyword", blank=True)
    poster_path = models.URLField(null=True)
    backdrop_path = models.URLField(null=True)
    recommendations = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Genre(QueryableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Language(QueryableModel):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Company(QueryableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"


class Keyword(QueryableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Contributor(QueryableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

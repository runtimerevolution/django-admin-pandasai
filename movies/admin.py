from adminfilters.filters import AutoCompleteFilter, ChoicesFieldComboFilter
from adminfilters.mixin import AdminFiltersMixin
from django.contrib import admin

from common.admin import YearListFilter
from movies.models import Company, Contributor, Genre, Keyword, Language, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Movie)
class MovieAdmin(AdminFiltersMixin, admin.ModelAdmin):
    search_fields = ["title"]
    list_display = [
        "title",
        "status",
        "release_date",
    ]
    list_filter = [
        ("release_date", YearListFilter),
        ("status", ChoicesFieldComboFilter),
        ("genres", AutoCompleteFilter),
        ("original_language", AutoCompleteFilter),
        ("production_companies", AutoCompleteFilter),
        ("credits", AutoCompleteFilter),
        ("keywords", AutoCompleteFilter),
        ("recommendations", AutoCompleteFilter),
    ]
    filter_horizontal = ["genres", "production_companies", "credits", "keywords", "recommendations"]
    ordering = ["title"]

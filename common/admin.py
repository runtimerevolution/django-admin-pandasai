from django.contrib import admin
from django.db import models
from django.db.models.functions import ExtractYear
from django.utils.translation import gettext_lazy as _


class YearListFilter(admin.FieldListFilter):
    template = "adminfilters/combobox.html"
    title = _("Year")

    def __init__(self, field, request, params, model, model_admin, field_path):
        queryset = model_admin.get_queryset(request)
        self.lookup_kwarg = f"{field_path}__year"
        self.lookup_kwarg_isnull = f"{field_path}__isnull"
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_choices = (
            queryset.filter(**{self.lookup_kwarg_isnull: False})
            .annotate(y=ExtractYear(field.name))
            .order_by(self.lookup_kwarg)
            .values_list(self.lookup_kwarg, flat=True)
            .distinct()
        )
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def get_facet_counts(self, pk_attname, filtered_qs):
        return {
            f"{i}__c": models.Count(
                pk_attname,
                filter=models.Q((self.lookup_kwarg, val) if val is not None else (self.lookup_kwarg_isnull, True)),
            )
            for i, val in enumerate(self.lookup_choices)
        }

    def choices(self, changelist):
        add_facets = changelist.add_facets
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None
        yield {
            "selected": self.lookup_val is None,
            "query_string": changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            "display": _("All"),
        }
        for i, val in enumerate(self.lookup_choices):
            title = val
            if add_facets:
                count = facet_counts[f"{i}__c"]
                title = f"{val} ({count})"
            yield {
                "selected": self.lookup_val is not None and str(val) in self.lookup_val,
                "query_string": changelist.get_query_string({self.lookup_kwarg: val}, [self.lookup_kwarg_isnull]),
                "display": title,
            }
